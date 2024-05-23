from datetime import timedelta
from django.db import models
from django.dispatch import receiver
from accounts.models import User
from django.db.models.signals import pre_save, post_save
import uuid, random
from django.utils import timezone
from django.utils import timezone
from django.db import models


# ACCESS KEYS FOR USERS
class AccessKey(models.Model):
    class KeyStatus(models.TextChoices):
        REVOKED = ("REVOKED", "Revoked")
        ACTIVE = ("ACTIVE", "Active")
        EXPIRED = ("EXPIRED", "Expired")

    key = models.UUIDField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expiry_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=10, choices=KeyStatus.choices, default=KeyStatus.ACTIVE
    )


# SET EXPIRY DATE AND KEY ON SAVE
@receiver(pre_save, sender=AccessKey)
def save_key_data(sender, instance, *args, **kwargs):
    if instance:
        instance.expiry_date = timezone.now() + timedelta(days=90)
        instance.key = uuid.uuid4()


# MANAGER TO CREATE KEY TOKEN
class KeyTokenManager(models.Manager):
    def create(self, **kwargs):
        instance = self.model(
            key="AKM_ACKY" + str(random.randrange(start=100, stop=10000)), **kwargs
        )
        instance.save()
        return instance


# KEYTOKENS TO BE SENT TO USERS FOR GENERATING ACCESS KEYS
class KeyToken(models.Model):

    class Status(models.TextChoices):
        ACTIVE = ("ACTIVE", "Active")
        EXPIRED = ("EXPIRED", "Expired")

    key = models.CharField(
        blank=True,
        null=True,
        unique=True,
        max_length=100,
        db_index=True,
    )
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, default=Status.ACTIVE, choices=Status.choices
    )

    objects = KeyTokenManager()
