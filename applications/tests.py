from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from accounts.models import UserProfile
from companies.models import Company
from jobs.models import Job


class CampusHireFlowTests(APITestCase):
    def register(self, username, role):
        r = self.client.post("/api/auth/register/", {
            "username": username, "email": f"{username}@x.com", "password": "Passw0rd!!", "role": role}, format="json")
        self.assertEqual(r.status_code, 201, r.data)
        return r.data["token"]

    def auth(self, token):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

    def test_full_flow(self):
        # recruiter creates company and job
        rec = self.register("rec", "recruiter")
        self.auth(rec)
        c = self.client.post("/api/companies/", {"name": "Acme", "description": "d"}, format="json")
        self.assertEqual(c.status_code, 201)
        j = self.client.post("/api/jobs/", {
            "company": c.data["id"], "title": "Dev", "description": "Build", "package_lpa": "6",
            "minimum_cgpa": "7", "eligible_departments": "CSE,IT", "maximum_backlogs": 0}, format="json")
        self.assertEqual(j.status_code, 201, j.data)
        job_id = j.data["id"]

        # student profile + eligibility
        stu = self.register("stu", "student")
        self.auth(stu)
        r = self.client.post(f"/api/applications/apply/{job_id}/")
        self.assertEqual(r.status_code, 400)  # no profile yet
        r = self.client.post("/api/students/profile/create/", {
            "roll_number": "r1", "department": "cse", "cgpa": "8.1", "backlogs": 0, "skills": "py"}, format="json")
        self.assertEqual(r.status_code, 201, r.data)
        jobs = self.client.get("/api/jobs/").data
        self.assertTrue(jobs[0]["eligible"])
        self.assertFalse(jobs[0]["applied"])
        r = self.client.post(f"/api/applications/apply/{job_id}/")
        self.assertEqual(r.status_code, 201, r.data)
        self.assertEqual(self.client.post(f"/api/applications/apply/{job_id}/").status_code, 400)  # duplicate
        app_id = self.client.get("/api/applications/mine/").data[0]["id"]

        # recruiter reviews
        self.auth(rec)
        apps = self.client.get("/api/applications/recruiter/").data
        self.assertEqual(apps[0]["roll_number"], "R1")
        r = self.client.patch("/api/applications/recruiter/", {"application_id": app_id, "status": "shortlisted"}, format="json")
        self.assertEqual(r.data["status"], "shortlisted")
        self.assertEqual(self.client.get("/api/jobs/mine/").data[0]["applications_count"], 1)

        # student cannot withdraw after shortlist
        self.auth(stu)
        self.assertEqual(self.client.delete(f"/api/applications/{app_id}/withdraw/").status_code, 400)

    def test_ineligible_student(self):
        rec_user = User.objects.create_user("r2", password="x")
        UserProfile.objects.create(user=rec_user, role="recruiter")
        co = Company.objects.create(recruiter=rec_user, name="Z")
        job = Job.objects.create(company=co, title="T", description="d", minimum_cgpa=9, eligible_departments="CSE")
        stu = self.register("s2", "student")
        self.auth(stu)
        self.client.post("/api/students/profile/create/", {"roll_number": "x1", "department": "ECE", "cgpa": "6", "backlogs": 2}, format="json")
        r = self.client.post(f"/api/applications/apply/{job.id}/")
        self.assertEqual(r.status_code, 400)
        self.assertIn("not eligible", r.data["detail"])

    def test_role_protection(self):
        stu = self.register("s3", "student")
        self.auth(stu)
        self.assertEqual(self.client.post("/api/companies/", {"name": "N"}, format="json").status_code, 403)
        self.client.credentials()
        self.assertEqual(self.client.get("/api/applications/mine/").status_code, 401)
        self.assertEqual(self.client.get("/api/jobs/").status_code, 200)
