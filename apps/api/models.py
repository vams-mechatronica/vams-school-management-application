from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


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

class TestAbhaResponse(models.Model):
    abha_address = models.CharField(max_length=500)
    link_token = models.TextField()
    response = models.TextField(_("Response"))
    created_at = models.DateTimeField(_("Created at"), auto_now=False, auto_now_add=True)
    

    class Meta:
        verbose_name = _("TEstAbhaResponse")
        verbose_name_plural = _("TEstAbhaResponses")

    def __str__(self):
        return self.abha_address

    def get_absolute_url(self):
        return reverse("TEstAbhaResponse_detail", kwargs={"pk": self.pk})
