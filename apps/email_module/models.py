from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


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

class EmailSentLogs(models.Model):
    to_emails = models.TextField(_("To emails"))
    template_name = models.CharField(_("Template Name"), max_length=50, null=True, blank=True)
    sent_at = models.DateTimeField(_("Sent at"), auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(_("Created At"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True, auto_now_add=False)
    
    class Meta:
        verbose_name = _("EmailSentLogs")
        verbose_name_plural = _("EmailSentLogs")

    def __str__(self):
        return "template_name: {} sent to (nos): {}".format(self.template_name, len(self.to_emails.split(',')))

    def get_absolute_url(self):
        return reverse("EmailSentLogs_detail", kwargs={"pk": self.pk})

