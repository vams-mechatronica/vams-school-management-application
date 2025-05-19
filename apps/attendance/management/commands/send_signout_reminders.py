# attendance/management/commands/send_signout_reminders.py

from django.core.management.base import BaseCommand
from attendance.utils import send_signout_reminder

class Command(BaseCommand):
    help = "Send reminder emails to users who have not signed out"

    def handle(self, *args, **kwargs):
        send_signout_reminder()
        self.stdout.write(self.style.SUCCESS("Sign-out reminder emails sent."))
