from django.db import models
from companies.models import Company


class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=150)
    description = models.TextField()
    location = models.CharField(max_length=120, blank=True)
    package_lpa = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    minimum_cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    eligible_departments = models.CharField(max_length=250, help_text="Comma-separated, e.g. IT,CSE")
    maximum_backlogs = models.PositiveIntegerField(default=0)
    required_skills = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def check_eligibility(self, profile):
        """Return (is_eligible, reason). Used by the jobs list and by apply."""
        if profile is None:
            return False, "Complete your student profile first"
        reasons = []
        if profile.cgpa < self.minimum_cgpa:
            reasons.append(f"Minimum CGPA is {self.minimum_cgpa}")
        depts = [d.strip().lower() for d in self.eligible_departments.split(",") if d.strip()]
        if depts and "all" not in depts and profile.department.strip().lower() not in depts:
            reasons.append("Your department is not eligible")
        if profile.backlogs > self.maximum_backlogs:
            reasons.append(f"Maximum {self.maximum_backlogs} backlogs allowed")
        return (not reasons), "; ".join(reasons)
