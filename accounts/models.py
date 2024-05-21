from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid, random
from django.utils import timezone


# CUSTOM USER MODEL MANAGER
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_registration_complete", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


# CUSTOM USER MODEL
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=128)


    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


# MANAGER TO CREATE EMAIL TOKEN
class EmailTokenManager(models.Manager):
    def create(self, **kwargs):
        code = random.randrange(1000, 10000)
        instance = self.model(code=code, **kwargs)
        instance.save()
        return instance


# EMAILTOKENS TO BE SENT TO USERS FOR EMAIL VERIFICATION
class EmailToken(models.Model):
    code = models.IntegerField(null=True, blank=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    objects = EmailTokenManager()

