from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def send_notification(mail_subject, mail_template, context):
    from_email = settings.EMAIL_HOST_USER
    message = render_to_string(mail_template, context)
    to_email = [context['to_email']]
    mail = EmailMessage(mail_subject, message, from_email, to=to_email)
    mail.content_subtype = "html"
    mail.send()
    print("mail sent")
