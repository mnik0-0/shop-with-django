from django.test import TestCase
from django.test import Client
from user.models import User
from catalog import models
from django.shortcuts import get_object_or_404
from django.http import Http404


class TestUrlsGet(TestCase):

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
        self.item = models.Item.objects.create(title='Phone', description='iphone11', slug='phone', tag=self.l_tag, user_id=user.id, price=10)
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

    def test_items_confirm_list_response(self):
        response = self.client.get('/items-confirm-list/')
        self.assertEqual(response.status_code, 200)

    def test_admin_panel_response(self):
        response = self.client.get('/admin-panel/')
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
        self.g_tag = models.GlobalTag.objects.create(title='Electronic')
        self.g_tag.save()
        self.l_tag = models.LocalTag.objects.create(title='Phone', global_tag=self.g_tag)
        self.l_tag.save()
        self.item = models.Item.objects.create(title='Phone', description='iphone11', slug='phone', tag=self.l_tag, user_id=user.id, price=10)
        self.item.save()

    def test_create_item_post(self):
        response = self.client.post('/create-item/', {'title': 'new phone', 'description': 'iphone10', 'tag': self.l_tag.id, 'price': 10})
        item = models.Item.objects.get(title__iexact='new phone')
        self.assertEqual(item.description, 'iphone10')
        self.assertEqual(item.tag, self.l_tag)

    def test_update_item_post(self):
        response = self.client.post('/item/phone/update/', {'title': 'old phone', 'description': 'iphone7', 'tag': self.l_tag.id, 'price': 10})
        item = models.Item.objects.get(title__iexact='old phone')
        self.assertEqual(item.description, 'iphone7')
        self.assertEqual(item.tag, self.l_tag)

    def test_create_global_tag_post(self):
        response = self.client.post('/create-global-tag/', {'title': 'Cars'})
        tag = models.GlobalTag.objects.get(title__iexact='Cars')

    def test_create_local_tag_post(self):
        response = self.client.post('/create-local-tag/', {'title': 'bmw', 'global_tag': self.g_tag.id})
        tag = models.LocalTag.objects.get(title__iexact='bmw')


class TestChangeUrls(TestCase):

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
        self.item = models.Item.objects.create(title='Phone', description='iphone11', slug='phone', tag=self.l_tag, user_id=user.id, price=10)
        self.item.save()


    def test_delete_tag(self):
        response = self.client.get('/tag/Phone/delete/')
        try:
            tag = get_object_or_404(models.LocalTag, title='Phone')
        except Http404:
            pass
        else:
            raise Http404('Didnt delete')


    def test_activate_item(self):
        self.assertEqual(get_object_or_404(models.Item, slug='phone').is_active, False)
        response = self.client.get('/item/phone/activate/')
        self.assertEqual(get_object_or_404(models.Item, slug='phone').is_active, True)


    def test_disactivate_item(self):
        self.item.is_active = True
        self.item.save()
        self.assertEqual(get_object_or_404(models.Item, slug='phone').is_active, True)
        response = self.client.get('/item/phone/disactivate/')
        self.assertEqual(get_object_or_404(models.Item, slug='phone').is_active, False)
