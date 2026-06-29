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


def notify(recipient, title, message, link=None):
    """Create a Notification for a single recipient.

    Notification (via BaseNotification) has no `user` or `link` field -
    only `delivery_type` and a `recipients` M2M - so the recipient is set
    via `recipients.add()` and the link is folded into the message text.
    """
    notification = Notification.objects.create(
        title=title,
        message=f"{message} {link}" if link else message,
        delivery_type="custom",
    )
    notification.recipients.add(recipient)
    return notification


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
            notify(
                admin,
                title="New Leave Request Submitted",
                message=f"{staff_user.get_full_name()} submitted a leave request from {instance.start_date} to {instance.end_date}.",
                link=instance.get_absolute_url(),
            )

        # Send email to approver
        send_html_email_async(
            template_name="new_leave_request",
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

        # send email to requester
        send_html_email_async(
            template_name="leave_request_submitted",
            to_emails=[staff_user.email],
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
            notify(
                staff_user,
                title="Leave Request Approved",
                message=f"Your leave request from {instance.start_date} to {instance.end_date} has been approved.",
                link=instance.get_absolute_url(),
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
            notify(
                staff_user,
                title="Leave Request Rejected",
                message=f"Your leave request from {instance.start_date} to {instance.end_date} has been rejected.",
                link=instance.get_absolute_url(),
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
