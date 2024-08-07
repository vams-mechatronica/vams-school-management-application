from django.db import models

# Create your models here.


class SiteConfig(models.Model):
    """Site Configurations"""

    key = models.SlugField()
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.key


class AcademicSession(models.Model):
    """Academic Session"""

    name = models.CharField(max_length=200, unique=True)
    current = models.BooleanField(default=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.current:
            AcademicSession.objects.filter(current=True).update(current=False)
        super().save(*args, **kwargs)


class AcademicTerm(models.Model):
    """Academic Term"""

    name = models.CharField(max_length=20, unique=True)
    current = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.current:
            AcademicTerm.objects.filter(current=True).update(current=False)
        super().save(*args, **kwargs)
    



class Subject(models.Model):
    """Subject"""

    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class StudentClass(models.Model):
    name = models.CharField(max_length=200, unique=True)
    tuition_fees = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    computer_fees = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    admission_fees = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    exam_fees = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    miscellaneous = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ["name"]

    def __str__(self):
        return self.name
