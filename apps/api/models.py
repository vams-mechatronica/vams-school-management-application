from django.db import models

# Create your models here.
class APKVersion(models.Model):
    version = models.CharField(max_length=10, unique=True)
    os = models.CharField(max_length=50, choices=(('android','Android'),('ios','iOS')),default="")
    file = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Version {self.version}"