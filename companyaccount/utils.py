from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from .token import account_activation_token
from django.contrib import messages


def send_approve_notification(mail_subject, mail_template, context):
    from_email = settings.EMAIL_HOST_USER
    message = render_to_string(mail_template, context)
    to_email = [context['to_email']]
    mail = EmailMessage(mail_subject, message, from_email, to=to_email)
    mail.content_subtype = "html"
    mail.send()
    print("mail sent")


def company_activation_mail(request, user_obj, company_user_form, ):
    print(" company_registration_mail called")
    current_site = get_current_site(request)
    subject = 'Welcome to JOBHUB!,Verify your Account.'
    message = render_to_string('company/acc_active_email.html', {
        'user': user_obj,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user_obj.pk)),
        'token': account_activation_token.make_token(user_obj),
    })
    recipient = company_user_form.cleaned_data.get('email')
    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
    print("company reg mail sent")
    messages.success(request, "An email has been send to you for account activation.")
