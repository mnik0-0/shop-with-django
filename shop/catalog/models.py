from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import time


# Create your models here.


class Item(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(default=time.time)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title


class ItemPhoto(models.Model):
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_photos', default='default_item_photo.jpg')

    def __str__(self):
        return self.item.title
