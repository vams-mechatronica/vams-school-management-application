from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

from .models import StaffLeaveRequest
from apps.notifications.models import Notification  # if you have a custom model
from apps.email_module.modules import send_html_email_async  # assuming your async function
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=StaffLeaveRequest)
def leave_request_notification(sender, instance, created, **kwargs):
    staff_user = instance.staff_user
    sitename = getattr(settings, 'SITE_NAME', 'School Portal')
    status = instance.status

    # Leave Submitted
    if created:
        # Notify admin or approver
        superusers = User.objects.filter(is_superuser=True)
        for admin in superusers:
            Notification.objects.create(
                user=admin,
                title="New Leave Request Submitted",
                message=f"{staff_user.get_full_name()} submitted a leave request from {instance.start_date} to {instance.end_date}.",
                link=instance.get_absolute_url()
            )

        # Send email to approver
        send_html_email_async(
            template_name="Leave Request Notification",
            to_emails=[admin.email for admin in superusers],
            content_context={
                "staff_name": staff_user.get_full_name(),
                "leave_type": "General Leave",  # or derive if you have a field
                "start_date": instance.start_date,
                "end_date": instance.end_date,
                "reason": instance.reason,
                "sitename": sitename,
                "leave_id": instance.pk
            }
        )

    # Leave Reviewed (Approved or Rejected)
    else:
        if status == 1:  # Approved
            Notification.objects.create(
                user=staff_user,
                title="Leave Request Approved",
                message=f"Your leave request from {instance.start_date} to {instance.end_date} has been approved.",
                link=instance.get_absolute_url()
            )

            send_html_email_async(
                template_name="Leave Request Approved",
                to_emails=[staff_user.email],
                content_context={
                    "staff_name": staff_user.get_full_name(),
                    "leave_type": "General Leave",
                    "start_date": instance.start_date,
                    "end_date": instance.end_date,
                    "reason": instance.reason,
                    "reviewed_by": instance.reviewed_by.get_full_name() if instance.reviewed_by else "Admin",
                    "sitename": sitename,
                    "current_year": timezone.now().year
                }
            )
        elif status == 2:  # Rejected
            Notification.objects.create(
                user=staff_user,
                title="Leave Request Rejected",
                message=f"Your leave request from {instance.start_date} to {instance.end_date} has been rejected.",
                link=instance.get_absolute_url()
            )

            send_html_email_async(
                template_name="Leave Request Rejected",
                to_emails=[staff_user.email],
                content_context={
                    "staff_name": staff_user.get_full_name(),
                    "leave_type": "General Leave",
                    "start_date": instance.start_date,
                    "end_date": instance.end_date,
                    "reason": instance.reason,
                    "reviewed_by": instance.reviewed_by.get_full_name() if instance.reviewed_by else "Admin",
                    "remarks": "",  # Add this if you allow remarks
                    "sitename": sitename,
                    "current_year": timezone.now().year
                }
            )
