from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Notification, Announcement, ShoutOut, DeliveredNotification

def deliver_to_users(instance, model_name):
    if instance.delivery_type == 'all':
        users = User.objects.all()
    else:
        users = instance.recipients.all()

    for user in users:
        DeliveredNotification.objects.create(
            user=user,
            content_type=model_name,
            object_id=instance.id
        )

@receiver(post_save, sender=Notification)
def notify_users(sender, instance, created, **kwargs):
    if created:
        deliver_to_users(instance, "Notification")

@receiver(post_save, sender=Announcement)
def announce_users(sender, instance, created, **kwargs):
    if created:
        deliver_to_users(instance, "Announcement")

@receiver(post_save, sender=ShoutOut)
def shoutout_users(sender, instance, created, **kwargs):
    if created:
        deliver_to_users(instance, "ShoutOut")
