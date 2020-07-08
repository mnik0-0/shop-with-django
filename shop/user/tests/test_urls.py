from django.test import TestCase
from django.test import Client
from user.models import User
from catalog import models
from django.shortcuts import get_object_or_404
from django.http import Http404


class TestUrls(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='my@gmail.com', name='me')
        self.user.set_password('my_password')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.client = Client()


    def test_registration_response(self):
        response = self.client.get('/user/registration/')
        self.assertEqual(response.status_code, 200)

    def test_registration_post(self):
        response = self.client.post('/user/registration/', {'email': 'check@gmail.com', 'name': 'NoName', 'password1': 'd6Fr64j75rGg37Jn', 'password2': 'd6Fr64j75rGg37Jn'})
        user = get_object_or_404(User, email='check@gmail.com')
        self.assertEqual(user.name, 'NoName')

    def test_login_response(self):
        response = self.client.get('/user/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_post(self):
        response = self.client.get('/items-confirm-list/')
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/user/login/', {'email': 'my@gmail.com', 'password': 'my_password'})
        response = self.client.get('/items-confirm-list/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get('/items-confirm-list/')
        self.assertEqual(response.status_code, 302)
        self.client.force_login(self.user)
        response = self.client.get('/items-confirm-list/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/user/logout/')
        response = self.client.get('/items-confirm-list/')
        self.assertEqual(response.status_code, 302)

    def test_profile_response(self):
        self.client.force_login(self.user)
        response = self.client.get(f'/user/profile/{self.user.profile.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_change_slug_response(self):
        self.client.force_login(self.user)
        response = self.client.get(f'/user/change-slug/')
        self.assertEqual(response.status_code, 200)

    def test_change_slug_post(self):
        self.client.force_login(self.user)
        response = self.client.post('/user/change-slug/', {'slug': 'newslug'})
        self.user = get_object_or_404(User, email='my@gmail.com')
        self.assertEqual(self.user.profile.slug, 'newslug')
