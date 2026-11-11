from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "recruiter", "website")
    search_fields = ("name", "recruiter__username")
