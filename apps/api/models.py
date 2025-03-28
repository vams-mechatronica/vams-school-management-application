from django.db import models
from django.utils.timezone import now

# Create your models here.
class APKVersion(models.Model):
    version = models.CharField(max_length=10, unique=True)
    os = models.CharField(max_length=50, choices=(('android','Android'),('ios','iOS')),default="")
    file = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Version {self.version}"
    

class ErrorLog(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    error = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    app_type = models.IntegerField(choices=[
        (0, '.apk'),
        (1, 'web'),(2, '.ios')],default=0)
    level = models.CharField(max_length=50, choices=[
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ])
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.level} - {self.error}"