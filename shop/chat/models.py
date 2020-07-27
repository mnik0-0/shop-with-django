from django.db import models
from django.conf import settings
from django.utils.timezone import now
from catalog.models import Item


# Create your models here.


class Chat(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chats')
    item = models.ForeignKey(Item, related_name='chats', on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=now)

    def __str__(self):
        return self.item.title


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='send_messages', on_delete=models.CASCADE)
    text = models.TextField(max_length=100)
    date = models.DateTimeField(auto_now=now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.chat.item.title
