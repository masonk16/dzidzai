from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Course


class OwnerMixin:

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin,
                       LoginRequiredMixin,
                       PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('courses:manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    """
    Lists the courses created by the user.
    """

    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """
    Uses a model form to create a new Course object.
    It uses the fields defined in OwnerCourseMixin
    to build a model form and also subclasses CreateView.
    It uses the template defined in OwnerCourseEditMixin.
    """
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """
    Allows the editing of an existing Course object.
    It uses the fields defined in OwnerCourseMixin to
    build a model form and also subclasses UpdateView.
    It uses the template defined in OwnerCourseEditMixin.
    """
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    """
    Inherits from OwnerCourseMixin and the generic DeleteView.
    It defines a specific template_name attribute for a template
    to confirm the course deletion.
    """

    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'