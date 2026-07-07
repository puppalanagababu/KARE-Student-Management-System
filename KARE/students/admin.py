from django.contrib import admin
from .models import Student, Attendance, Marks, Timetable


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "roll_number",
        "department",
        "year",
        "email",
        "phone",
    )

    search_fields = (
        "name",
        "roll_number",
        "department",
    )

    list_filter = (
        "department",
        "year",
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "date",
        "status",
    )

    list_filter = (
        "status",
        "date",
    )

    search_fields = (
        "student__name",
    )


@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "subject",
        "internal",
        "external",
        "total",
        "grade",
    )

    search_fields = (
        "student__name",
        "subject",
    )

    list_filter = (
        "grade",
    )


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "day",
        "subject",
        "time",
    )

    list_filter = (
        "day",
    )

    search_fields = (
        "student__name",
        "subject",
    )