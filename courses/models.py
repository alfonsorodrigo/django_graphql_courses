from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=100)
    year_of_publication = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)

class Student(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
