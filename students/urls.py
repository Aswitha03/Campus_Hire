from django.urls import path
from . import views
urlpatterns=[path("profile/",views.profile),path("profile/create/",views.create_profile)]
