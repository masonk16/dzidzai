"""
Models for Courses application.
"""
from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    """
    Subject - high level owner of course and module.
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return str(self.title)


class Course(models.Model):
    """
    Section of the subject matter.
    """

    owner = models.ForeignKey(
        User, related_name="courses_created", on_delete=models.CASCADE
        )
    subject = models.ForeignKey(
        Subject, related_name="courses", on_delete=models.CASCADE
        )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return str(self.title)


class Module(models.Model):
    """
    Section/Chapter of the course.
    """

    course = models.ForeignKey(
        Course, related_name="modules", on_delete=models.CASCADE
        )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.title)
