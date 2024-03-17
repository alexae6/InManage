from django.urls import path
from . import views

app_name = "base" 

urlpatterns = [
    path("home/", views.home, name="home"),
    path("patientinfo/<str:entry>", views.patientinfo, name="patientinfo"),
    path("upload/", views.upload, name="upload"),
    path("monthly/", views.monthly, name="monthly"),
    path("calendar/", views.calendar, name="calendar"),
    path("register/", views.register_request, name="register"),
    path("", views.login_request, name="login"),
    path("searchpatient/", views.searchpatient,name="searchpatient")
]