"""
Models for Courses application.
"""
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


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

    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.title)


class Content(models.Model):
    """
    Stores different content for the modules.
    """

    module = models.ForeignKey(
        Module, related_name="contents", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")


class ItemBase(models.Model):
    """
    Abstract model for content management.
    """
    owner = models.ForeignKey(
        User, related_name="%(class)s_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.title)


class Text(ItemBase):
    """
    Text content management.
    """
    content = models.TextField()


class File(ItemBase):
    """
    File content management.
    """
    file = models.FileField(upload_to="files")


class Image(ItemBase):
    """
    Image content management.
    """
    file = models.FileField(upload_to="images")


class Video(ItemBase):
    """
    Video content management.
    """
    url = models.URLField()
