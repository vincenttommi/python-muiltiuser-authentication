from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token  # Correct import
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


# Custom User model with boolean fields for role identification
class User(AbstractUser):
    is_freelancer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# Automatically create a token for the user when they are created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Freelancer model linked to User with a OneToOneField
class Freelancer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="freelancer")  # Proper on_delete behavior
    phone = models.CharField(max_length=50, null=True, blank=True)
    skills = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    portfolio = models.CharField(max_length=100, null=True, blank=True)  # Corrected typo from 'portofolio' to 'portfolio'

    def __str__(self):
        return self.user.username


# Client model linked to User with a OneToOneField
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client")  # Proper on_delete behavior
    company_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.company_name
