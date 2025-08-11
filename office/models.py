from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, related_name='sections', on_delete=models.CASCADE)
    short_name = models.CharField(max_length=50, null=True)


    def __str__(self):
        return f"{self.department.name} - {self.name}"


class Unit(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50, null=True)
    def __str__(self):
        return self.name
