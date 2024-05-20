from django.core.mail import EmailMessage
from accounts.models import EmailToken
from django.conf import settings

# SEND CONFIRMATION CODE TO USER
def send_confirmation_code(user):
    email_token = EmailToken.objects.create(user=user)
    message = f""" Hi {user.username},
    There's one quick step you need to complete before creating your account.PLease enter this verification code to confirm this is your email.
    {email_token.code}
    """
    email = EmailMessage(
        to=[user.email],
        body=message,
        reply_to=[settings.EMAIL_HOST_USER],
        from_email=settings.EMAIL_HOST_USER,
        subject="Verify Email Accounts",
    )
    email.send(fail_silently=False)
    return
