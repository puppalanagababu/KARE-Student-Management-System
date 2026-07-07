from django.shortcuts import render, redirect
from .models import Student
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models import Count, Q
from django.core.paginator import Paginator

def student_list(request):

    query = request.GET.get("q")
    department = request.GET.get("department")
    year = request.GET.get("year")

    students = Student.objects.all()

    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(roll_number__icontains=query)
        )

    if department:
        students = students.filter(department=department)

    if year:
        students = students.filter(year=year)

    departments = Student.objects.values_list(
        "department",
        flat=True
    ).distinct()

    years = Student.objects.values_list(
        "year",
        flat=True
    ).distinct()
    paginator = Paginator(students, 10)

    page_number = request.GET.get("page")

    students = paginator.get_page(page_number)

    return render(request, "student_list.html", {

        "students": students,

        "query": query,

        "departments": departments,

        "years": years,

        "selected_department": department,

        "selected_year": year,

    })
def add_student(request):

    if request.method == "POST":

        name = request.POST.get("name")
        roll_number = request.POST.get("roll_number")
        department = request.POST.get("department")
        year = request.POST.get("year")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        photo = request.FILES.get("photo")

        Student.objects.create(
            name=name,
            roll_number=roll_number,
            department=department,
            year=year,
            email=email,
            phone=phone,
            photo=photo

        )

        return redirect("/students/")

    return render(request, "add_student.html")

def edit_student(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":

        student.name = request.POST.get("name")
        student.roll_number = request.POST.get("roll_number")
        student.department = request.POST.get("department")
        student.year = request.POST.get("year")
        student.email = request.POST.get("email")
        student.phone = request.POST.get("phone")
        photo = request.FILES.get("photo")
    if photo:
        student.photo = photo

        student.save()

        return redirect("/students/")

    return render(request, "edit_student.html", {
        "student": student
    })
from django.db.models import Q

def student_list(request):

    query = request.GET.get("q")

    students = Student.objects.all()

    if query:

        students = Student.objects.filter(

            Q(name__icontains=query) |

            Q(roll_number__icontains=query) |

            Q(department__icontains=query)

        )

    return render(request, "student_list.html", {

        "students": students,

        "query": query

    })

def student_detail(request, id):

    student = get_object_or_404(Student, id=id)

    attendance = Attendance.objects.filter(student=student)

    marks = Marks.objects.filter(student=student)

    timetable = Timetable.objects.filter(student=student)

    return render(request, "student_detail.html", {

        "student": student,

        "attendance": attendance,

        "marks": marks,

        "timetable": timetable,

    })

from .models import Student, Attendance

def attendance_list(request):

    attendance = Attendance.objects.all()

    return render(request, "attendance_list.html", {
        "attendance": attendance
    })

def attendance_report(request):

    students = Student.objects.all()

    report = []

    for student in students:

        total = Attendance.objects.filter(student=student).count()

        present = Attendance.objects.filter(
            student=student,
            status="Present"
        ).count()

        absent = Attendance.objects.filter(
            student=student,
            status="Absent"
        ).count()

        if total > 0:
            percentage = (present / total) * 100
        else:
            percentage = 0

        if percentage >= 75:
            status = "Excellent"
            color = "success"

        elif percentage >= 50:
            status = "Average"
            color = "warning"

        else:
            status = "Low Attendance"
            color = "danger"

        report.append({

            "student": student,

            "present": present,

            "absent": absent,

            "total": total,

            "percentage": round(percentage, 2),

            "status": status,

            "color": color,

        })

    return render(request, "attendance_report.html", {

        "report": report

    })
from .models import Student, Attendance, Marks

def marks_list(request):

    marks = Marks.objects.all()

    return render(request, "marks_list.html", {
        "marks": marks
    })
from .models import Student, Attendance, Marks, Timetable

def timetable_list(request):

    timetable = Timetable.objects.all()

    return render(request, "timetable.html", {
        "timetable": timetable
    })

from reportlab.pdfgen import canvas
from django.http import HttpResponse
def export_students_pdf(request):

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="students.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold",18)

    p.drawString(180,800,"KARE STUDENT REPORT")

    p.setFont("Helvetica",12)

    y = 760

    students = Student.objects.all()

    for student in students:

        p.drawString(

            50,

            y,

            f"{student.name} | {student.roll_number} | {student.department}"

        )

        y -= 25

        if y < 50:

            p.showPage()

            y = 800

    p.save()

    return response
from openpyxl import Workbook
def export_excel(request):

    wb = Workbook()

    ws = wb.active

    ws.title = "Students"

    ws.append([
        "Name",
        "Roll Number",
        "Department",
        "Year",
        "Email",
        "Phone"
    ])

    students = Student.objects.all()

    for student in students:

        ws.append([
            student.name,
            student.roll_number,
            student.department,
            student.year,
            student.email,
            student.phone
        ])

    response = HttpResponse(

        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )

    response["Content-Disposition"] = 'attachment; filename="students.xlsx"'

    wb.save(response)

    return response

def delete_student(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.delete()
        return redirect("/students/")

    return render(request, "delete_student.html", {
        "student": student
    })

def report_card(request, id):

    student = get_object_or_404(Student, id=id)

    marks = Marks.objects.filter(student=student)

    total_marks = 0

    subject_count = marks.count()

    for mark in marks:
        total_marks += mark.total

    if subject_count > 0:
        average = round(total_marks / subject_count, 2)
    else:
        average = 0

    if average >= 90:
        overall_grade = "A+"
    elif average >= 80:
        overall_grade = "A"
    elif average >= 70:
        overall_grade = "B"
    elif average >= 60:
        overall_grade = "C"
    else:
        overall_grade = "D"

    return render(request, "report_card.html", {

        "student": student,

        "marks": marks,

        "total_marks": total_marks,

        "average": average,

        "overall_grade": overall_grade,

    })