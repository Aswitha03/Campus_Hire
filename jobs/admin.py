from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "package_lpa", "minimum_cgpa", "is_active")
    list_filter = ("is_active", "company")
    search_fields = ("title", "company__name")
