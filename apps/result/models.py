from django.db import models

from apps.corecode.models import (
    AcademicSession,
    AcademicTerm,
    StudentClass,
    Subject,
)
from apps.students.models import Student

from .utils import score_grade


# Create your models here.
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    current_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test_score = models.IntegerField(default=0)
    exam_score = models.IntegerField(default=0)

    class Meta:
        ordering = ["subject"]

    def __str__(self):
        return f"{self.student} {self.session} {self.term} {self.subject}"

    def total_score(self):
        return self.test_score + self.exam_score

    def grade(self):
        return score_grade(self.total_score())
    
    def calc_grade(self):
        t_max = self.subject.test_max_marks + self.subject.exam_max_marks
        t_ob = self.total_score()
        perc = (float(t_ob) / float(t_max)) * 100
        if perc == 100:
            grade = 'A+'
        elif perc <100 and perc >= 90:
            grade = 'A'
        elif perc < 90 and perc >= 80:
            grade = 'B+'
        elif perc < 80 and perc >= 70:
            grade = 'B'
        
        elif perc < 70 and perc >= 60:
            grade = 'C+'
        
        elif perc < 60 and perc >= 50:
            grade = 'C'
        
        elif perc < 50 and perc >= 40:
            grade = 'D+'
        elif perc < 40 and perc >= 33:
            grade = 'D'
        else:
            grade = 'F'
        return grade
