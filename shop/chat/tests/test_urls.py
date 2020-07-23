from django.test import TestCase
from django.test import Client
from user.models import User
from catalog import models as catalog
from chat import models


class TestUrlsGet(TestCase):

    def setUp(self):
        user = User.objects.create(email='my@gmail.com', name='me')
        user.set_password('my_password')
        user.is_superuser = True
        user.is_staff = True
        user.save()
        self.client = Client()
        self.client.force_login(user)
        user2 = User.objects.create(email='my2@gmail.com', name='me')
        user2.set_password('my_password')
        user2.is_superuser = True
        user2.is_staff = True
        user2.save()
        self.client2 = Client()
        self.client2.force_login(user2)
        self.g_tag = catalog.GlobalTag.objects.create(title='Electronic')
        self.g_tag.save()
        self.l_tag = catalog.LocalTag.objects.create(title='Phone', global_tag=self.g_tag)
        self.l_tag.save()
        self.item = catalog.Item.objects.create(title='Phone', description='iphone11', slug='phone', tag=self.l_tag, user_id=user.id, price=10)
        self.item.save()
        self.chat = models.Chat.objects.create(item=self.item)
        self.chat.users.add(user)
        self.chat.users.add(user2)
        self.chat.save()


    def test_chat_list_reponse(self):
        response = self.client.get('/chat/')
        self.assertEqual(response.status_code, 200)

    def test_chat_view_response(self):
        response = self.client.get(f'/chat/{self.item.slug}/')
        self.assertEqual(response.status_code, 200)


class TestUrlsPost(TestCase):

    def setUp(self):
        user = User.objects.create(email='my@gmail.com', name='me')
        user.set_password('my_password')
        user.is_superuser = True
        user.is_staff = True
        user.save()
        self.client = Client()
        self.client.force_login(user)
        user2 = User.objects.create(email='my2@gmail.com', name='me')
        user2.set_password('my_password')
        user2.is_superuser = True
        user2.is_staff = True
        user2.save()
        self.client2 = Client()
        self.client2.force_login(user2)
        self.g_tag = catalog.GlobalTag.objects.create(title='Electronic')
        self.g_tag.save()
        self.l_tag = catalog.LocalTag.objects.create(title='Phone', global_tag=self.g_tag)
        self.l_tag.save()
        self.item = catalog.Item.objects.create(title='Phone', description='iphone11', slug='phone', tag=self.l_tag, user_id=user.id, price=10)
        self.item.save()
        self.chat = models.Chat.objects.create(item=self.item)
        self.chat.users.add(user)
        self.chat.users.add(user2)
        self.chat.save()
        self.sender = user


    def test_send_message_post(self):
        response = self.client.post(f'/chat/{self.item.slug}/', {'text': 'message'})
        message = models.Message.objects.get(text='message')
        self.assertEqual(message.chat, self.chat)
        self.assertEqual(message.sender, self.sender)
