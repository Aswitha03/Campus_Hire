// Shared helpers used by every page.
// Change API_BASE to the deployed backend URL before publishing the frontend.
const API_BASE = "http://127.0.0.1:8000";

const getToken = () => localStorage.getItem("campushire_token");
const getUser = () => JSON.parse(localStorage.getItem("campushire_user") || "null");

function saveSession(data) {
  localStorage.setItem("campushire_token", data.token);
  localStorage.setItem("campushire_user", JSON.stringify(data.user));
}

// Turn a DRF error body ({field:[msg]} or {detail:msg}) into one readable string.
function errorText(d) {
  if (!d || typeof d !== "object") return "Something went wrong";
  if (d.detail) return d.detail;
  return Object.entries(d).map(([k, v]) => `${k}: ${[].concat(v).join(" ")}`).join(" | ");
}

// request("/api/jobs/")  or  request("/api/x/", {method:"POST", body:{...}})
// body may be a plain object (sent as JSON) or FormData (file upload).
async function request(path, opts = {}) {
  const headers = { ...(opts.headers || {}) };
  if (getToken()) headers.Authorization = "Token " + getToken();
  let body = opts.body;
  if (body && !(body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
    body = JSON.stringify(body);
  }
  let res;
  try {
    res = await fetch(API_BASE + path, { ...opts, headers, body });
  } catch (e) {
    throw Error("Cannot reach the server. Is the Django backend running?");
  }
  if (res.status === 204) return null;
  const data = await res.json().catch(() => ({}));
  if (res.status === 401 && getToken()) {        // token expired or deleted
    localStorage.clear();
    location.href = "login.html";
  }
  if (!res.ok) throw Error(errorText(data));
  return data;
}

// Escape text before putting it inside innerHTML (prevents XSS).
function safe(s) {
  return String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function toast(message, isError = false) {
  let t = document.getElementById("toast");
  if (!t) { t = document.createElement("div"); t.id = "toast"; document.body.appendChild(t); }
  t.textContent = message;
  t.className = "show" + (isError ? " err" : "");
  clearTimeout(t._timer);
  t._timer = setTimeout(() => (t.className = ""), 3000);
}

function dashboardUrl(user) {
  return user.role === "recruiter" ? "recruiter-dashboard.html" : "student-dashboard.html";
}

async function logout() {
  try { await request("/api/auth/logout/", { method: "POST" }); } catch (e) { /* ignore */ }
  localStorage.clear();
  location.href = "index.html";
}

// Redirect to login unless a user with the given role is signed in.
function requireRole(role) {
  const u = getUser();
  if (!getToken() || !u) { location.href = "login.html"; return null; }
  if (u.role !== role) { location.href = dashboardUrl(u); return null; }
  return u;
}

// Draw the header on every page: <header id="site-header"></header>
function renderHeader() {
  const h = document.getElementById("site-header");
  if (!h) return;
  const u = getUser();
  const page = location.pathname.split("/").pop() || "index.html";
  const link = (href, text) => `<a href="${href}" class="${page === href ? "active" : ""}">${text}</a>`;
  let nav = link("jobs.html", "Jobs");
  if (u && getToken()) {
    nav += link(dashboardUrl(u), "Dashboard") + `<span class="hint">${safe(u.username)}</span><button id="logout">Logout</button>`;
  } else {
    nav += link("login.html", "Login") + `<a class="btn small" href="register.html">Register</a>`;
  }
  h.innerHTML = `<a class="brand" href="index.html">Campus<span>Hire</span></a><nav>${nav}</nav>`;
  const b = document.getElementById("logout");
  if (b) b.onclick = logout;
}
document.addEventListener("DOMContentLoaded", renderHeader);
