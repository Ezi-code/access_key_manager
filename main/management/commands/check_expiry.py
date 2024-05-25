from main.models import AccessKey
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


class Command(BaseCommand):
    help = "Check for expired access keys and send email to the user"

    def handle(self, *args, **kwargs):
        keys = AccessKey.objects.all()
        for expired_key in keys:
            if (
                expired_key.status == AccessKey.KeyStatus.ACTIVE
                and expired_key.expiry_date < timezone.now()
            ):
                expired_key.status = AccessKey.KeyStatus.EXPIRED
                expired_key.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Access key {expired_key.key} has expired")
                )
                send_mail(
                    "Access Key Expired",
                    f"Your access key {expired_key.key} has expired",
                    settings.EMAIL_HOST_USER,
                    [expired_key.user.email],
                    fail_silently=False,
                )
                return self.stdout.write(self.style.SUCCESS("Email sent to user"))
        return self.stdout.write(self.style.SUCCESS("No expired keys found"))
