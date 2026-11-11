from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.username", read_only=True)
    student_email = serializers.CharField(source="student.email", read_only=True)
    job_title = serializers.CharField(source="job.title", read_only=True)
    company_name = serializers.CharField(source="job.company.name", read_only=True)
    roll_number = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    cgpa = serializers.SerializerMethodField()
    backlogs = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()
    resume_url = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            "id", "student", "student_name", "student_email", "job", "job_title", "company_name",
            "roll_number", "department", "cgpa", "backlogs", "skills", "resume_url",
            "status", "applied_at",
        ]
        read_only_fields = ["id", "student", "status", "applied_at"]

    def _p(self, obj):
        return getattr(obj.student, "student_profile", None)

    def get_roll_number(self, obj):
        p = self._p(obj)
        return p.roll_number if p else None

    def get_department(self, obj):
        p = self._p(obj)
        return p.department if p else None

    def get_cgpa(self, obj):
        p = self._p(obj)
        return str(p.cgpa) if p else None

    def get_backlogs(self, obj):
        p = self._p(obj)
        return p.backlogs if p else None

    def get_skills(self, obj):
        p = self._p(obj)
        return p.skills if p else None

    def get_resume_url(self, obj):
        p = self._p(obj)
        if p and p.resume:
            request = self.context.get("request")
            return request.build_absolute_uri(p.resume.url) if request else p.resume.url
        return None
