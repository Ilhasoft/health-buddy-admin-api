from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def send_email_recover_password(sender, instance, reset_password_token, *args, **kwargs):
    subject = "test"
    from_email = "mieldazis@ilhasoft.com.br"
    to = "s.mieldazis@hotmail.com"

    context = {"key": "value"}

    html_content = render_to_string("email/email_forgot_password.html", context)
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
