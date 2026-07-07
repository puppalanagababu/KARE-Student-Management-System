from django.db import models


# -----------------------------
# Student Model
# -----------------------------
class Student(models.Model):

    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    year = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    # Student Photo
    photo = models.ImageField(
        upload_to="students/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


# -----------------------------
# Attendance Model
# -----------------------------
class Attendance(models.Model):

    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    def __str__(self):
        return f"{self.student.name} - {self.date}"


# -----------------------------
# Marks Model
# -----------------------------
class Marks(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    subject = models.CharField(max_length=100)

    internal = models.IntegerField()

    external = models.IntegerField()

    total = models.IntegerField()

    grade = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.student.name} - {self.subject}"


# -----------------------------
# Timetable Model
# -----------------------------
class Timetable(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    day = models.CharField(max_length=20)

    subject = models.CharField(max_length=100)

    time = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.student.name} - {self.day}"