from django.db import models

class EmailTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Internal name for reference.")
    subject = models.CharField(max_length=255, help_text="Subject of the email.")
    body = models.TextField(help_text="HTML body. You can use Django template variables like {{ name }}, {{ message }}.")
    is_active = models.BooleanField(default=True, help_text="If unchecked, this template will not be used.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Email Template"
        verbose_name_plural = "Email Templates"
        ordering = ['name']

    def __str__(self):
        return self.name
