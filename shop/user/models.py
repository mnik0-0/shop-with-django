from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.user.username

    @classmethod
    def get(cls, request, slug):
        object = get_object_or_404(UserProfile, slug__iexact=slug)
        return object
