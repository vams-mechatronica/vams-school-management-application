from django.db import models
from django.contrib.auth.models import User

DELIVERY_CHOICES = (
    ('all', 'All Users'),
    ('custom', 'Custom Users'),
)

class BaseNotification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    delivery_type = models.CharField(max_length=10, choices=DELIVERY_CHOICES)
    recipients = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Notification(BaseNotification):

    class Meta:
        verbose_name = 'Notifications'
        verbose_name_plural = 'Notifications'


class Announcement(BaseNotification):
    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'

class ShoutOut(BaseNotification):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shoutouts_sent')

    class Meta:
        verbose_name = 'ShoutOut'
        verbose_name_plural = 'ShoutOuts'

class DeliveredNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=50)
    object_id = models.PositiveIntegerField()
    delivered_at = models.DateTimeField(auto_now_add=True)
    mark_as_read = models.BooleanField(default=False)
