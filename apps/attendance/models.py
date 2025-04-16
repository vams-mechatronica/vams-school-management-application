from django.db import models
from django.urls import reverse,reverse_lazy
from django.utils.translation import gettext_lazy as _
from apps.students.models import Student
from apps.staffs.models import Staff
from datetime import date

# Create your models here.
class StudentAttendance(models.Model):
    ATTENDANCE_CHOICE = ((1, 'Present'),(0,'Absent'),(2, 'On-leave'),(3, 'Other'))
    student = models.ForeignKey(Student, verbose_name=_("Student Name"), on_delete=models.CASCADE)
    date = models.DateField(_("Date"), auto_now=False, auto_now_add=False)
    status = models.IntegerField(_("Status"),choices=ATTENDANCE_CHOICE, default=0)
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
    ATTENDANCE_CHOICE = ((1, 'Present'),(0,'Absent'),(2, 'On-leave'),(3, 'Other'))
    staff = models.ForeignKey(Staff, verbose_name=_("Staff Name"), on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    status = models.IntegerField(_("Status"),choices=ATTENDANCE_CHOICE, default=0)
    time_in = models.TimeField(_("Time-In"),null=True,blank=True)
    time_out = models.TimeField(_("Time-Out"),null=True,blank=True)
    remarks = models.CharField(_("Remarks"), max_length=500,null=True,blank=True)
    created_at = models.DateTimeField(_("Created_at"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated_at"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("StaffAttendance")
        verbose_name_plural = _("StaffAttendances")

    def __str__(self):
        return "{first_name} {last_name} Time: In: {time_in} Out: {time_out}".format(first_name =self.staff.firstname, last_name=self.staff.surname, time_in= self.time_in, time_out=self.time_out)

    def get_absolute_url(self):
        return reverse("StaffAttendance_detail", kwargs={"pk": self.pk})

