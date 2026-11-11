// Student dashboard: profile (with resume upload) and my applications.
const me = requireRole("student");
const form = document.getElementById("profile");
const msgEl = document.getElementById("msg");
let hasProfile = false;

function say(text, isError) {
  msgEl.textContent = text;
  msgEl.className = isError ? "error" : "ok";
}

async function loadProfile() {
  try {
    const p = await request("/api/students/profile/");
    hasProfile = true;
    for (const k of ["roll_number", "department", "cgpa", "backlogs", "skills"]) form.elements[k].value = p[k] ?? "";
    document.getElementById("resume-link").innerHTML = p.resume
      ? `Current resume: <a href="${safe(p.resume)}" target="_blank">View PDF</a>` : "No resume uploaded yet.";
    document.getElementById("profile-note").textContent = "";
  } catch (e) {
    hasProfile = false;
    document.getElementById("profile-note").textContent =
      "Fill in your profile to check eligibility and apply for jobs.";
  }
}

async function loadApplications() {
  const box = document.getElementById("apps");
  try {
    const apps = await request("/api/applications/mine/");
    const count = s => apps.filter(a => a.status === s).length;
    document.getElementById("n-total").textContent = apps.length;
    document.getElementById("n-short").textContent = count("shortlisted");
    document.getElementById("n-sel").textContent = count("selected");
    if (!apps.length) { box.innerHTML = `<p class="empty">No applications yet. <a href="jobs.html">Browse jobs</a></p>`; return; }
    box.innerHTML = `<div class="table-wrap"><table><thead><tr><th>Job</th><th>Company</th><th>Applied on</th><th>Status</th><th></th></tr></thead><tbody>` +
      apps.map(a => `<tr>
        <td>${safe(a.job_title)}</td><td>${safe(a.company_name)}</td>
        <td>${new Date(a.applied_at).toLocaleDateString()}</td>
        <td><span class="badge ${safe(a.status)}">${safe(a.status)}</span></td>
        <td>${a.status === "applied" ? `<button class="btn danger small" onclick="withdraw(${a.id})">Withdraw</button>` : ""}</td>
      </tr>`).join("") + `</tbody></table></div>`;
  } catch (e) {
    box.innerHTML = `<p class="error">${safe(e.message)}</p>`;
  }
}

async function withdraw(id) {
  if (!confirm("Withdraw this application?")) return;
  try {
    await request(`/api/applications/${id}/withdraw/`, { method: "DELETE" });
    toast("Application withdrawn");
    loadApplications();
  } catch (e) { toast(e.message, true); }
}

form.onsubmit = async e => {
  e.preventDefault();
  const fd = new FormData(form);
  if (!fd.get("resume") || !fd.get("resume").name) fd.delete("resume");   // nothing chosen
  try {
    await request(hasProfile ? "/api/students/profile/" : "/api/students/profile/create/",
      { method: hasProfile ? "PATCH" : "POST", body: fd });
    say("Profile saved", false);
    form.elements.resume.value = "";
    await loadProfile();
  } catch (x) { say(x.message, true); }
};

if (me) { loadProfile(); loadApplications(); }
