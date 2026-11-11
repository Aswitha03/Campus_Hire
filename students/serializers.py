from rest_framework import serializers
from .models import StudentProfile

MAX_RESUME_MB = 2


class StudentProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = StudentProfile
        fields = ["id", "username", "email", "roll_number", "department", "cgpa", "backlogs", "skills", "resume"]
        read_only_fields = ["id"]

    def validate_cgpa(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError("CGPA must be between 0 and 10")
        return value

    def validate_department(self, value):
        return value.strip().upper()

    def validate_roll_number(self, value):
        return value.strip().upper()

    def validate_resume(self, f):
        if f is None:
            return f
        if not f.name.lower().endswith(".pdf"):
            raise serializers.ValidationError("Resume must be a PDF file")
        if f.size > MAX_RESUME_MB * 1024 * 1024:
            raise serializers.ValidationError(f"Resume must be smaller than {MAX_RESUME_MB} MB")
        return f
