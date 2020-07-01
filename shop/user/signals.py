from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import time
from django.contrib.auth import get_user_model


@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created, **kwargs):
    if created:
        models.UserProfile.objects.create(user=instance, slug=time.time())

@receiver(post_save, sender=get_user_model())
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
