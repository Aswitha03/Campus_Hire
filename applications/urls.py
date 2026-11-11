from django.urls import path
from . import views

urlpatterns = [
    path("apply/<int:job_id>/", views.apply),
    path("mine/", views.mine),
    path("<int:pk>/withdraw/", views.withdraw),
    path("recruiter/", views.recruiter),
]
