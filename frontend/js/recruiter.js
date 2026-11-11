// Recruiter dashboard: companies, post jobs, manage jobs, review applicants.
const recruiter = requireRole("recruiter");
let companies = [];
let myJobs = [];

const val = (form, name) => form.elements[name].value.trim();

// ---------- companies ----------
async function loadCompanies() {
  companies = await request("/api/companies/mine/");
  document.getElementById("company-list").innerHTML = companies.length
    ? companies.map(c => `<span class="chip">${safe(c.name)}</span>`).join(" ")
    : `<p class="empty">Create a company first, then you can post jobs.</p>`;
  document.getElementById("job-company").innerHTML =
    companies.map(c => `<option value="${c.id}">${safe(c.name)}</option>`).join("");
  document.getElementById("job-form").querySelector("button").disabled = !companies.length;
}

document.getElementById("company-form").onsubmit = async e => {
  e.preventDefault();
  const f = e.target;
  try {
    await request("/api/companies/", { method: "POST", body: {
      name: val(f, "name"), description: val(f, "description"), website: val(f, "website") } });
    f.reset();
    toast("Company created");
    loadCompanies();
  } catch (x) { toast(x.message, true); }
};

// ---------- jobs ----------
document.getElementById("job-form").onsubmit = async e => {
  e.preventDefault();
  const f = e.target;
  const body = Object.fromEntries(new FormData(f));
  try {
    await request("/api/jobs/", { method: "POST", body });
    f.reset();
    toast("Job posted");
    loadJobs();
  } catch (x) { toast(x.message, true); }
};

async function loadJobs() {
  myJobs = await request("/api/jobs/mine/");
  const box = document.getElementById("job-list");
  document.getElementById("n-jobs").textContent = myJobs.length;
  document.getElementById("filter-job").innerHTML = `<option value="">All jobs</option>` +
    myJobs.map(j => `<option value="${j.id}">${safe(j.title)}</option>`).join("");
  if (!myJobs.length) { box.innerHTML = `<p class="empty">No jobs posted yet.</p>`; loadApplicants(); return; }
  box.innerHTML = `<div class="table-wrap"><table><thead><tr><th>Title</th><th>Company</th><th>Package</th><th>Applicants</th><th>Status</th><th></th></tr></thead><tbody>` +
    myJobs.map(j => `<tr>
      <td>${safe(j.title)}</td><td>${safe(j.company_name)}</td><td>${safe(j.package_lpa)} LPA</td>
      <td>${j.applications_count}</td>
      <td><span class="badge ${j.is_active ? "eligible" : "closed"}">${j.is_active ? "open" : "closed"}</span></td>
      <td>
        <button class="btn ghost small" onclick="toggleJob(${j.id}, ${!j.is_active})">${j.is_active ? "Close" : "Reopen"}</button>
        <button class="btn danger small" onclick="deleteJob(${j.id})">Delete</button>
      </td></tr>`).join("") + `</tbody></table></div>`;
  loadApplicants();
}

async function toggleJob(id, active) {
  try { await request(`/api/jobs/${id}/`, { method: "PATCH", body: { is_active: active } }); loadJobs(); }
  catch (x) { toast(x.message, true); }
}

async function deleteJob(id) {
  if (!confirm("Delete this job and all its applications?")) return;
  try { await request(`/api/jobs/${id}/`, { method: "DELETE" }); toast("Job deleted"); loadJobs(); }
  catch (x) { toast(x.message, true); }
}

// ---------- applicants ----------
async function loadApplicants() {
  const jobId = document.getElementById("filter-job").value;
  const box = document.getElementById("applicants");
  try {
    const apps = await request("/api/applications/recruiter/" + (jobId ? `?job=${jobId}` : ""));
    document.getElementById("n-apps").textContent = apps.length;
    if (!apps.length) { box.innerHTML = `<p class="empty">No applications yet.</p>`; return; }
    box.innerHTML = `<div class="table-wrap"><table><thead><tr><th>Student</th><th>Job</th><th>Dept / CGPA</th><th>Skills</th><th>Resume</th><th>Status</th><th>Action</th></tr></thead><tbody>` +
      apps.map(a => `<tr>
        <td><b>${safe(a.student_name)}</b><br><span class="hint">${safe(a.roll_number)} · ${safe(a.student_email)}</span></td>
        <td>${safe(a.job_title)}<br><span class="hint">${safe(a.company_name)}</span></td>
        <td>${safe(a.department)}<br>${safe(a.cgpa)} · ${safe(a.backlogs)} backlog(s)</td>
        <td>${safe(a.skills)}</td>
        <td>${a.resume_url ? `<a href="${safe(a.resume_url)}" target="_blank">PDF</a>` : "—"}</td>
        <td><span class="badge ${safe(a.status)}">${safe(a.status)}</span></td>
        <td>
          <button class="btn small ghost" onclick="setStatus(${a.id}, 'shortlisted')">Shortlist</button>
          <button class="btn small" onclick="setStatus(${a.id}, 'selected')">Select</button>
          <button class="btn small danger" onclick="setStatus(${a.id}, 'rejected')">Reject</button>
        </td></tr>`).join("") + `</tbody></table></div>`;
  } catch (x) { box.innerHTML = `<p class="error">${safe(x.message)}</p>`; }
}

async function setStatus(id, status) {
  try {
    await request("/api/applications/recruiter/", { method: "PATCH", body: { application_id: id, status } });
    toast("Marked " + status);
    loadApplicants();
  } catch (x) { toast(x.message, true); }
}

document.getElementById("filter-job").onchange = loadApplicants;

if (recruiter) loadCompanies().then(loadJobs).catch(x => toast(x.message, true));
