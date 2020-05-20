from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def send_email_recover_password(sender, instance, reset_password_token, *args, **kwargs):
    subject = "Forgot password - Healthbuddy Admin"
    to = reset_password_token.user.email
    from_email = settings.DEFAULT_FROM_EMAIL

    context = {"token": reset_password_token.key, "username": reset_password_token.user.username}

    html_content = render_to_string("email/email_forgot_password.html", context)
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
