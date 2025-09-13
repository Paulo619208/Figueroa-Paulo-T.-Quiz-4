from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


# ✅ FIXED: Simplified the UserManager to work with Django's built-in fields
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


# ✅ FIXED: Simplified the CustomUser model to use Django's built-in fields
class CustomUser(AbstractUser):
    # We remove the username field to use email as the unique identifier
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No extra fields required besides email and password

    objects = UserManager()

    def __str__(self):
        return self.email


# ✅ FIXED: Corrected the Profile model and image upload path
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    # This simplified path is safe and works correctly
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')

    def __str__(self):
        return f'{self.user.email} Profile'