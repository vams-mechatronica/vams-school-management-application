from django.db import models
from apps.corecode.models import StudentClass, Subject
from apps.students.models import Student
from apps.staffs.models import Staff
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

DAY_CHOICES = [
        (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'),
        (4, 'Thursday'), (5, 'Friday'),(6,'Saturday')
    ]

# Create your models here.
class Period(models.Model):
    name = models.CharField(_("Periods"), max_length=50)

    class Meta:
        verbose_name = _("Period")
        verbose_name_plural = _("Periods")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Period_detail", kwargs={"pk": self.pk})

class PeriodDay(models.Model):
    day = models.IntegerField(_("day"), choices=DAY_CHOICES)
    number_of_periods = models.IntegerField(_("no_of_periods"),default=0)
    
    class Meta:
        verbose_name = _("PeriodDay")
        verbose_name_plural = _("PeriodDays")

    def __str__(self):
        return "{} - {}".format(self.day,self.number_of_periods)

    def get_absolute_url(self):
        return reverse("PeriodDay_detail", kwargs={"pk": self.pk})

class Timetable(models.Model):
    
    day = models.IntegerField(choices=DAY_CHOICES)
    period = models.ForeignKey(Period, verbose_name=_("Period"), on_delete=models.CASCADE)
    class_assigned = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, verbose_name=_("Subject"), on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.class_assigned.name} - {self.day} - {self.period}"