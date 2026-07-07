from django.urls import path
from . import views

urlpatterns = [

    # -------------------------
    # Website Pages
    # -------------------------

    path("", views.home, name="home"),

    path("about/", views.about, name="about"),

    path("admissions/", views.admissions, name="admissions"),

    path("academics/", views.academics, name="academics"),

    path("placements/", views.placements, name="placements"),

    path("gallery/", views.gallery, name="gallery"),

    path("contact/", views.contact, name="contact"),


    # -------------------------
    # Authentication
    # -------------------------

    path("login/", views.student_login, name="login"),

    path("register/", views.register, name="register"),

    path("logout/", views.student_logout, name="logout"),


    # -------------------------
    # Dashboards
    # -------------------------

    path("dashboard/", views.dashboard, name="dashboard"),

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "faculty-dashboard/",
        views.faculty_dashboard,
        name="faculty_dashboard"
    ),

]