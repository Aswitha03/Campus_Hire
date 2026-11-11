// Login and register forms.
const loginForm = document.getElementById("login");
const registerForm = document.getElementById("register");
const msg = document.getElementById("msg");

async function submitAuth(form, url) {
  msg.textContent = "";
  const btn = form.querySelector("button");
  btn.disabled = true;
  try {
    const data = await request(url, { method: "POST", body: Object.fromEntries(new FormData(form)) });
    saveSession(data);
    location.href = dashboardUrl(data.user);
  } catch (e) {
    msg.textContent = e.message;
    msg.className = "error";
  } finally {
    btn.disabled = false;
  }
}

if (getToken() && getUser() && (loginForm || registerForm)) location.href = dashboardUrl(getUser());
if (loginForm) loginForm.onsubmit = e => { e.preventDefault(); submitAuth(loginForm, "/api/auth/login/"); };
if (registerForm) registerForm.onsubmit = e => { e.preventDefault(); submitAuth(registerForm, "/api/auth/register/"); };
