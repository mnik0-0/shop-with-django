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
