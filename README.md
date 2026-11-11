# CampusHire starter project
Django REST Framework + HTML/CSS/JavaScript placement portal teaching MVP.

## Windows setup
```powershell
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```
Edit `.env` and set a strong random SECRET_KEY.
```bash
python manage.py makemigrations accounts students companies jobs applications
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Optional: load demo data (recruiter1 / Recruiter@123, student1 / Student@123):
```bash
python manage.py seed_demo
```
Run the tests: `python manage.py test`

In another terminal:
```bash
cd frontend
py -m http.server 5500
```
Open http://127.0.0.1:5500

## API
POST `/api/auth/register/` JSON `{username,email,password,role}` where role is student or recruiter.
POST `/api/auth/login/` JSON `{username,password}`.
GET `/api/auth/me/` token required.
POST `/api/students/profile/create/` create profile; GET/PATCH `/api/students/profile/`.
POST `/api/auth/logout/` token required (deletes the token).
GET/POST `/api/companies/` (POST recruiter token). GET `/api/companies/mine/` recruiter.
GET `/api/jobs/?q=python&min_package=5` public; POST recruiter token (include company id). Students also get `eligible`, `eligibility_reason`, `applied`.
GET `/api/jobs/mine/` recruiter (all own jobs + `applications_count`).
GET/PATCH/DELETE `/api/jobs/<id>/` (PATCH/DELETE: owner recruiter only).
POST `/api/applications/apply/<job_id>/` student token.
GET `/api/applications/mine/` student token.
DELETE `/api/applications/<id>/withdraw/` student, only while status is `applied`.
GET/PATCH `/api/applications/recruiter/` recruiter token (`?job=<id>` filter); PATCH `{application_id,status}`.
Resume upload: send `multipart/form-data` with a `resume` PDF (max 2 MB) to the student profile endpoints.

## Pages
`index.html`, `register.html`, `login.html`, `jobs.html` (search, eligibility, apply), `student-dashboard.html` (profile, resume, applications), `recruiter-dashboard.html` (companies, post jobs, close/delete jobs, shortlist/select/reject applicants).

## Create recruiter company/job
Register as recruiter, open the recruiter dashboard, add a company, then post a job.

## Team split
Student 1: accounts and students apps.
Student 2: companies, jobs and applications apps.
Student 3: frontend folder and integration.
All: API contract, testing, pull requests, documentation and deployment.

## Deployment
Push project to GitHub. Render backend root is repository root. Build:
`pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
Start:
`gunicorn config.wsgi:application`
Set SECRET_KEY, DEBUG=False, DATABASE_URL, ALLOWED_HOSTS, CORS_ALLOWED_ORIGINS in Render. Create Render PostgreSQL and use its Internal Database URL. Deploy frontend as Render Static Site with root directory `frontend` and publish directory `.`. Update `frontend/js/api.js` API_BASE to backend URL and add frontend URL to CORS_ALLOWED_ORIGINS. Redeploy.

## Production warning
This is a teaching MVP starter, not a security-audited production system. Add tests, stronger role/ownership permissions, safe resume storage, rate limits, password reset, email verification, backups, monitoring and privacy controls before real student data is used. Never commit `.env` or credentials.
