from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)
    company_website = serializers.CharField(source="company.website", read_only=True)
    # Filled only for logged-in students (see jobs/views.py -> build_context)
    eligible = serializers.SerializerMethodField()
    eligibility_reason = serializers.SerializerMethodField()
    applied = serializers.SerializerMethodField()
    # Filled only on the recruiter "mine" endpoint (annotated count)
    applications_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Job
        fields = [
            "id", "company", "company_name", "company_website", "title", "description", "location",
            "package_lpa", "minimum_cgpa", "eligible_departments", "maximum_backlogs",
            "required_skills", "is_active", "eligible", "eligibility_reason", "applied",
            "applications_count",
        ]
        read_only_fields = ["id", "company"]

    def validate_minimum_cgpa(self, v):
        if v < 0 or v > 10:
            raise serializers.ValidationError("CGPA must be between 0 and 10")
        return v

    def validate_package_lpa(self, v):
        if v < 0:
            raise serializers.ValidationError("Package cannot be negative")
        return v

    def _ctx(self):
        return self.context if self.context.get("is_student") else None

    def get_eligible(self, job):
        c = self._ctx()
        return None if c is None else job.check_eligibility(c["profile"])[0]

    def get_eligibility_reason(self, job):
        c = self._ctx()
        return None if c is None else job.check_eligibility(c["profile"])[1]

    def get_applied(self, job):
        c = self._ctx()
        return None if c is None else job.id in c["applied_ids"]
