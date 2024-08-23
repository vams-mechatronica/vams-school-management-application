from django.db import models
from django.utils.translation import gettext_lazy as _
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
    test_max_marks = models.IntegerField(_("Test Maximum Marks"),default=50)
    exam_max_marks = models.IntegerField(_("Exam Maximum Marks"),default=100)

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


class EmailMessageImageLink(models.Model):
    image_1 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_2 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_3 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_4 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_5 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_6 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_7 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_8 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_9 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_10 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_11 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_12 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_13 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_14 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_15 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_16 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_17 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_18 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_19 = models.ImageField(upload_to='email/images/',blank=True,null=True)
    image_20 = models.ImageField(upload_to='email/images/',blank=True,null=True)

    class Meta:
        verbose_name = _("EmailMessageImageLink")
        verbose_name_plural = _("EmailMessageImageLinks")

    def __str__(self):
        return self.pk

