from django.test import TestCase
from django.test import Client
from user.models import User
from catalog import models


class TestForms(TestCase):

    def setUp(self):
        user = User.objects.create(email='my@gmail.com', name='me')
        user.set_password('my_password')
        user.is_superuser = True
        user.is_staff = True
        user.save()
        self.client = Client()
        self.client.force_login(user)
        self.g_tag = models.GlobalTag.objects.create(title='Electronic')
        self.g_tag.save()
        self.l_tag = models.LocalTag.objects.create(title='Phone', global_tag=self.g_tag)
        self.l_tag.save()
        self.item = models.Item.objects.create(title='Phone', description='iphone11', slug='phone', tag=self.l_tag, user_id=user.id)
        self.item.save()

    def test_create_item_form(self):
        response = self.client.post('/create-item/', {'title': 'new phone', 'description': 'iphone10', 'tag': self.l_tag.id}) # self.l_tag have vlaue 9
        item = models.Item.objects.get(title__iexact='new phone')
        self.assertEqual(item.description, 'iphone10')
        self.assertEqual(item.tag, self.l_tag)

    def test_update_item_form(self):
        response = self.client.post('/item/phone/update/', {'title': 'old phone', 'description': 'iphone7', 'tag': self.l_tag.id})
        item = models.Item.objects.get(title__iexact='old phone')
        self.assertEqual(item.description, 'iphone7')
        self.assertEqual(item.tag, self.l_tag)

    def test_create_global_tag_tag_form(self):
        response = self.client.post('/create-global-tag/', {'title': 'Cars'})
        tag = models.GlobalTag.objects.get(title__iexact='Cars')

    def test_create_global_tag_tag_form(self):
        response = self.client.post('/create-local-tag/', {'title': 'bmw', 'global_tag': self.g_tag.id})
        tag = models.LocalTag.objects.get(title__iexact='bmw')
