from django.test import TestCase
from django.test import Client
from user.models import User
from catalog import models

class TestUrlsResponseGet(TestCase):

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

    def test_index_response(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_item_response(self):
        response = self.client.get('/create-item/')
        self.assertEqual(response.status_code, 200)

    def test_update_item_response(self):
        response = self.client.get('/item/phone/update/')
        self.assertEqual(response.status_code, 200)

    def test_item_slug_response(self):
        response = self.client.get('/item/phone/')
        self.assertEqual(response.status_code, 200)

    def test_tag_response(self):
        response = self.client.get('/tag/')
        self.assertEqual(response.status_code, 200)

    def test_tag_slug_response(self):
        response = self.client.get('/tag/phone/')
        self.assertEqual(response.status_code, 200)

    def test_create_global_tag_response(self):
        response = self.client.get('/create-global-tag/')
        self.assertEqual(response.status_code, 200)

    def test_create_local_tag_response(self):
        response = self.client.get('/create-local-tag/')
        self.assertEqual(response.status_code, 200)
