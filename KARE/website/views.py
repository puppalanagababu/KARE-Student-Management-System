from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Department, News, Contact
from students.models import Student, Attendance, Marks, Timetable
from django.core.mail import send_mail
from django.conf import settings


def home(request):

    departments = Department.objects.all()
    news = News.objects.all()

    return render(request, "home.html", {
        "departments": departments,
        "news": news,
    })


def about(request):
    return render(request, "about.html")


def admissions(request):
    return render(request, "admissions.html")


def academics(request):
    return render(request, "academics.html")


def placements(request):
    return render(request, "placements.html")


def gallery(request):
    return render(request, "gallery.html")


def contact(request):

    if request.method == "POST":

        Contact.objects.create(

            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            message=request.POST.get("message")

        )

        messages.success(request, "Message sent successfully!")

    return render(request, "contact.html")


# ---------------- LOGIN ---------------- #

def student_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.groups.filter(name="Admin").exists():
                return redirect("/admin-dashboard/")

            elif user.groups.filter(name="Faculty").exists():
                return redirect("/faculty-dashboard/")

            else:
                return redirect("/dashboard/")

        else:

            messages.error(request, "Invalid Username or Password")

    return render(request, "login.html")


# ---------------- REGISTER ---------------- #

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        send_mail(

    "Welcome to KARE Portal",

    f"""
Hello {username},

Welcome to KARE Portal.

Your registration was successful.

Thank you.

KARE Portal Team
""",

    settings.EMAIL_HOST_USER,

    [email],

    fail_silently=False,

)

        if password1 == password2:

            if User.objects.filter(username=username).exists():

                messages.error(request, "Username already exists.")

            else:

                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1
                )

                messages.success(request, "Registration Successful!")

                return redirect("/login/")

        else:

            messages.error(request, "Passwords do not match.")

    return render(request, "register.html")


# ---------------- LOGOUT ---------------- #

def student_logout(request):

    logout(request)

    return redirect("/")


# ---------------- DASHBOARD ---------------- #
@login_required
def dashboard(request):

    context = {

        "student_count": Student.objects.count(),

        "attendance_count": Attendance.objects.count(),

        "marks_count": Marks.objects.count(),

        "timetable_count": Timetable.objects.count(),

        "department_count": Department.objects.count(),

        "news_count": News.objects.count(),

        "recent_students": Student.objects.order_by("-id")[:5],

    }

    return render(request, "dashboard.html", context)

@login_required
def admin_dashboard(request):

    return render(request, "admin_dashboard.html")


@login_required
def faculty_dashboard(request):

    return render(request, "faculty_dashboard.html")