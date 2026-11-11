"""Create demo data so the project can be shown without typing anything.

    python manage.py seed_demo

Logins created:
    recruiter1 / Recruiter@123
    student1   / Student@123   (CSE, CGPA 8.2)
    student2   / Student@123   (ECE, CGPA 6.4)
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from accounts.models import UserProfile
from applications.models import Application
from companies.models import Company
from jobs.models import Job
from students.models import StudentProfile


def make_user(username, password, role):
    user, created = User.objects.get_or_create(username=username, defaults={"email": f"{username}@example.com"})
    if created:
        user.set_password(password)
        user.save()
    UserProfile.objects.get_or_create(user=user, defaults={"role": role})
    return user


class Command(BaseCommand):
    help = "Load demo users, companies, jobs and applications"

    def handle(self, *args, **options):
        recruiter = make_user("recruiter1", "Recruiter@123", "recruiter")

        s1 = make_user("student1", "Student@123", "student")
        StudentProfile.objects.get_or_create(user=s1, defaults=dict(
            roll_number="21CS001", department="CSE", cgpa=8.2, backlogs=0,
            skills="Python, Django, SQL, HTML, CSS, JavaScript"))
        s2 = make_user("student2", "Student@123", "student")
        StudentProfile.objects.get_or_create(user=s2, defaults=dict(
            roll_number="21EC014", department="ECE", cgpa=6.4, backlogs=1,
            skills="C, Embedded Systems, Python"))

        companies = {}
        for name, desc, site in [
            ("TechNova", "Product company building SaaS tools for schools.", "https://technova.example.com"),
            ("DataWorks", "Analytics and AI consulting firm.", "https://dataworks.example.com"),
            ("CloudSpring", "Cloud infrastructure and DevOps services.", "https://cloudspring.example.com"),
        ]:
            companies[name], _ = Company.objects.get_or_create(
                name=name, recruiter=recruiter, defaults={"description": desc, "website": site})

        jobs = [
            ("TechNova", "Python Django Developer", "Bengaluru", 6, 7.0, "CSE,IT", 0,
             "Python, Django, REST, SQL", "Build and maintain REST APIs for our learning platform."),
            ("TechNova", "Frontend Developer", "Hyderabad", 5, 6.5, "CSE,IT,ECE", 1,
             "HTML, CSS, JavaScript", "Create responsive interfaces with plain JavaScript and modern CSS."),
            ("DataWorks", "Data Analyst Trainee", "Chennai", 4.5, 6.0, "CSE,IT,ECE,EEE", 2,
             "SQL, Excel, Python", "Clean, analyse and visualise client data."),
            ("DataWorks", "ML Engineer", "Pune", 9, 8.0, "CSE,IT", 0,
             "Python, Machine Learning, Pandas", "Train and deploy machine learning models."),
            ("CloudSpring", "DevOps Engineer", "Hyderabad", 7, 7.0, "CSE,IT,ECE", 0,
             "Linux, Docker, Git, CI/CD", "Automate builds and deployments on the cloud."),
        ]
        created_jobs = []
        for company, title, loc, pkg, cgpa, depts, backlogs, skills, desc in jobs:
            job, _ = Job.objects.get_or_create(
                company=companies[company], title=title,
                defaults=dict(location=loc, package_lpa=pkg, minimum_cgpa=cgpa,
                              eligible_departments=depts, maximum_backlogs=backlogs,
                              required_skills=skills, description=desc))
            created_jobs.append(job)

        Application.objects.get_or_create(student=s1, job=created_jobs[0])
        self.stdout.write(self.style.SUCCESS("Demo data ready. Logins: recruiter1 / Recruiter@123, student1 / Student@123"))
