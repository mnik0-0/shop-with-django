from django.db import models
from django.utils import timezone
from django.shortcuts import get_object_or_404
import time
from django.conf import settings
from django.contrib.auth import get_user_model


# Create your models here.

def time_to_str():
    return str(time.time()).replace('.', '')


class Tag(models.Model):
    title = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class GlobalTag(Tag):
    pass


class LocalTag(Tag):
    global_tag = models.ForeignKey(GlobalTag, related_name='local_tags', on_delete=models.SET_NULL, null=True)


class Item(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField(max_length=300)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    slug = models.SlugField(default=time_to_str)
    date_pub = models.DateTimeField(default=timezone.now)
    date_upd = models.DateTimeField(default=timezone.now)
    tag = models.ForeignKey(LocalTag, related_name='items', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class ItemPhoto(models.Model):
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_photos', default='default_item_photo.jpg')

    def __str__(self):
        return self.item.title
