# attendance/utils.py

from django.utils import timezone
from apps.email_module.modules import send_html_email_async
from django.conf import settings
from .models import StaffAttendance
import logging
logger = logging.getLogger(__name__)

def send_signout_reminder():
    now = timezone.now()
    today = now.date()
    

    # You may filter by time to send it only after a certain time of day
    if now.hour > 13:  # Only run this after 1 PM
        return

    # Get attendances with time_in but no time_out
    missing_signouts = StaffAttendance.objects.filter(date=today, status=1, time_out__isnull=True)
    sitename = getattr(settings, 'SITE_NAME', 'School Portal')

    for record in missing_signouts:
        user = record.staff.user  # Assuming StaffAttendance has staff_user FK → Staff → user
        email = user.email
        if email:
            logger.info("sending email to: {}".format(email))
            send_html_email_async(to_emails=[email],template_name="signout_reminder",content_context={
                "user_name": user.get_full_name() or user.username,
                "date": timezone.now().date().strftime('%B %d, %Y'),
                "year": timezone.now().year,
                "site_name": sitename

            })
            
