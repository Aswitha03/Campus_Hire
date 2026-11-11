from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("roll_number", "user", "department", "cgpa", "backlogs")
    list_filter = ("department",)
    search_fields = ("roll_number", "user__username")
