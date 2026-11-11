// Public jobs page: search, eligibility badge and apply button.
const list = document.getElementById("jobs");
const msgBox = document.getElementById("msg");
const user = getUser();

function jobCard(j) {
  const skills = (j.required_skills || "").split(",").map(s => s.trim()).filter(Boolean)
    .map(s => `<span class="chip gray">${safe(s)}</span>`).join("");
  let action;
  if (!user) action = `<a class="btn small" href="login.html">Login to apply</a>`;
  else if (user.role !== "student") action = "";
  else if (j.applied) action = `<span class="badge applied">Applied</span>`;
  else if (!j.eligible) action = `<span class="badge noteligible" title="${safe(j.eligibility_reason)}">Not eligible</span>`;
  else action = `<button class="btn small" onclick="applyTo(${j.id}, this)">Apply</button>`;
  const why = user && user.role === "student" && !j.eligible && !j.applied
    ? `<p class="hint">${safe(j.eligibility_reason)}</p>` : "";
  return `<article>
    <h3>${safe(j.title)}</h3>
    <p class="company">${safe(j.company_name)}${j.location ? " · " + safe(j.location) : ""}</p>
    <div class="meta">
      <span class="chip">${safe(j.package_lpa)} LPA</span>
      <span class="chip gray">CGPA ≥ ${safe(j.minimum_cgpa)}</span>
      <span class="chip gray">Backlogs ≤ ${safe(j.maximum_backlogs)}</span>
      <span class="chip gray">${safe(j.eligible_departments)}</span>
    </div>
    <p class="job-desc">${safe(j.description)}</p>
    <div class="meta">${skills}</div>
    ${why}
    <div class="card-foot">${action}</div>
  </article>`;
}

async function loadJobs() {
  const q = document.getElementById("q").value.trim();
  const pkg = document.getElementById("pkg").value;
  const params = new URLSearchParams();
  if (q) params.set("q", q);
  if (pkg) params.set("min_package", pkg);
  try {
    const jobs = await request("/api/jobs/?" + params);
    list.innerHTML = jobs.map(jobCard).join("");
    msgBox.textContent = jobs.length ? `${jobs.length} job(s) found` : "No jobs found.";
    msgBox.className = "hint";
  } catch (e) {
    msgBox.textContent = e.message;
    msgBox.className = "error";
  }
}

async function applyTo(id, btn) {
  btn.disabled = true;
  try {
    await request(`/api/applications/apply/${id}/`, { method: "POST" });
    toast("Applied successfully");
    loadJobs();
  } catch (e) {
    toast(e.message, true);
    btn.disabled = false;
  }
}

let timer;
document.getElementById("q").oninput = () => { clearTimeout(timer); timer = setTimeout(loadJobs, 300); };
document.getElementById("pkg").onchange = loadJobs;
loadJobs();
