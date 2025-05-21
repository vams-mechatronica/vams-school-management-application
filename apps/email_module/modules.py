import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.template import Template, Context
from .models import EmailTemplate, EmailSentLogs
from datetime import datetime,timezone
import logging
logger = logging.getLogger(__name__)

def send_html_email_async(template_name, to_emails,content_context):
    """
    Sends an HTML email using threading.
    
    :param subject: Email subject
    :param to_emails: List of recipient email addresses
    :param content_context: Context dictionary for rendering the HTML template
    :param template: Path to the HTML template (default is 'email_module/base_template.html')
    """
    def send_email():
        try:
            email_template_data = EmailTemplate.objects.get(name=template_name)
            subject = email_template_data.subject.replace('__schoolname__', content_context.get('sitename', ''))
            template_string = email_template_data.body
            html_template = Template(template_string)
            html_content = html_template.render(Context(content_context))
            
            msg = EmailMultiAlternatives(subject, '', settings.DEFAULT_FROM_EMAIL, to_emails)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            # save log 
            sent_log = EmailSentLogs.objects.create(to_emails = to_emails, template_name=template_name, sent_at=datetime.now())
        except Exception as e:
            # Log or handle exception
            logger.error(f"Email sending failed: {e}")

    thread = threading.Thread(target=send_email)
    thread.start()
