from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import time


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        models.UserProfile.objects.create(user=instance, slug=time.time())

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
