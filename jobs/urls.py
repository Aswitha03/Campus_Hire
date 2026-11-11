from django.urls import path
from . import views

urlpatterns = [
    path("", views.jobs),
    path("mine/", views.my_jobs),
    path("<int:pk>/", views.job_detail),
]
