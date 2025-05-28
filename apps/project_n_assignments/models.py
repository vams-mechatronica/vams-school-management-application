from django.db import models
from apps.students.models import Student, StudentClass
from apps.staffs.models import Staff
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


# Create your models here.
class ClassAssignmentNProject(models.Model):
    name = models.CharField(_("Title"), max_length=500)
    file = models.FileField(_("Upload File"), upload_to='assignments/', max_length=100, help_text="Upload only .pdf, .txt, .docx, .jpg or .jpeg file only")
    for_class = models.ForeignKey(StudentClass, verbose_name=_("Class"), on_delete=models.CASCADE, help_text="Upload file of maxsize upto 10MBs only.")
    is_assignment_for_all = models.BooleanField(_("All Students"), default=True, help_text="If assignment/project is for all students of selected class.")
    students = models.ManyToManyField(Student, verbose_name=_("Students"), null=True)
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    due_date = models.DateField(_("Due Date"), auto_now=True, auto_now_add=False)
    is_active = models.BooleanField(_("Is Active"),default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("ClassAssignmentNProject")
        verbose_name_plural = _("ClassAssignmentNProjects")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ClassAssignmentNProject_detail", kwargs={"pk": self.pk})

class StudentAssignmentStatus(models.Model):
    assignment = models.ForeignKey('ClassAssignmentNProject', on_delete=models.CASCADE, related_name='student_assignments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_submitted = models.BooleanField(default=False)
    submitted_file = models.FileField(upload_to='assignments/submissions/', null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('assignment', 'student')
        verbose_name = _("Student Assignment Status")
        verbose_name_plural = _("Student Assignment Statuses")

    def __str__(self):
        return f"{self.student} - {self.assignment.name}"