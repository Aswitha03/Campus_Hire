from django.urls import path
from . import views

urlpatterns = [
    path("", views.companies),
    path("mine/", views.my_companies),
]
