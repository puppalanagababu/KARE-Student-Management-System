from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
class Contact(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=15)

    message = models.TextField()

    def __str__(self):
        return self.name