from django.urls import path
from . import views

urlpatterns = [
    path("", views.student_list, name="student_list"),

    path("add/", views.add_student, name="add_student"),
    path("edit/<int:id>/", views.edit_student, name="edit_student"),
    path("delete/<int:id>/", views.delete_student, name="delete_student"),
    path("detail/<int:id>/", views.student_detail, name="student_detail"),

    path("attendance/", views.attendance_list, name="attendance"),
    path("attendance-report/", views.attendance_report, name="attendance_report"),

    path("marks/", views.marks_list, name="marks_list"),
    path("timetable/", views.timetable_list, name="timetable_list"),

    path("export-pdf/", views.export_students_pdf, name="export_pdf"),
    path("export-excel/", views.export_excel, name="export_excel"),

    path(
        "report-card/<int:id>/",
        views.report_card,
        name="report_card",
    ),
]