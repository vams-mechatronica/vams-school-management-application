from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from apps.students.models import Student
from apps.staffs.models import Staff

# Create your models here.
class StudentAttendance(models.Model):
    ATTENDANCE_CHOICE = (('present', 'Present'),('absent','Absent'),('on-leave', 'On-leave'),('other', 'Other'))
    student = models.ForeignKey(Student, verbose_name=_("Student Name"), on_delete=models.CASCADE)
    date = models.DateField(_("Date"), auto_now=False, auto_now_add=False)
    status = models.CharField(_("Status"), max_length=50, blank=True,null=True,choices=ATTENDANCE_CHOICE)
    remarks = models.CharField(_("Remarks"), max_length=500,null=True,blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now=False, auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("StudentAttendance")
        verbose_name_plural = _("StudentAttendances")

    def __str__(self):
        return "{registration} {student_name} {date} {status}".format(registration=self.student.registration_number,student_name=self.student.firstname,date=self.date,status=self.status)

    def get_absolute_url(self):
        return reverse("StudentAttendance_detail", kwargs={"pk": self.pk})
    

class StaffAttendance(models.Model):
    ATTENDANCE_CHOICE = (('present', 'Present'),('absent','Absent'),('on-leave', 'On-leave'),('other', 'Other'))
    staff = models.ForeignKey(Staff, verbose_name=_("Staff Name"), on_delete=models.CASCADE)
    status = models.CharField(_("Status"), max_length=50, blank=True,null=True,choices=ATTENDANCE_CHOICE)
    time_in = models.DateTimeField(_("Time-In"), auto_now=False, auto_now_add=True)
    time_out = models.DateTimeField(_("Time-Out"), auto_now=True, auto_now_add=False)
    remarks = models.CharField(_("Remarks"), max_length=500,null=True,blank=True)

    class Meta:
        verbose_name = _("StaffAttendance")
        verbose_name_plural = _("StaffAttendances")

    def __str__(self):
        return "{first_name} {last_name} Time: In: {time_in} Out: {time_out}".format(first_name =self.staff.firstname, last_name=self.staff.surname, time_in= self.time_in, time_out=self.time_out)

    def get_absolute_url(self):
        return reverse("StaffAttendance_detail", kwargs={"pk": self.pk})

