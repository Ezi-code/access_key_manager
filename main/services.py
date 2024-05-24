import time
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from main.models import KeyToken, AccessKey
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone


# SEND KEY TOKEN TO USER


def send_key_token(user):
    token_instance = KeyToken.objects.create(user=user)
    message = f"""Hi {user.username},
        Your Access Key Generation token is {token_instance.key}.
        Please verify to generate a new Access Token for your system to continue usage.
        Thank you.
    """
    mail = EmailMessage(
        to=[user.email],
        body=message,
        reply_to=[settings.EMAIL_HOST_USER],
        from_email=settings.EMAIL_HOST_USER,
        subject="Verify Access Key Token",
    )
    mail.send(fail_silently=False)
    return True


class LoginMixin(LoginRequiredMixin):
    def get_login_url(self):
        return reverse_lazy("accounts:login_page")
