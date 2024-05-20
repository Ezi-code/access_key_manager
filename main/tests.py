from django.test import TestCase
from main.models import AccessKey
from main.views import *
from django.http import request
from django.shortcuts import render

# Create your tests here.
from django.test import TestCase
from accounts.models import User
from main.models import AccessKey


class AccessKeyTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@demo.com", password="testpassword"
        )
        self.access_key = AccessKey.objects.create(user=self.user, status="ACTIVE")

    def test_save_key_data(self):
        self.assertIsNotNone(self.access_key.expiry_date)
        self.assertIsNotNone(self.access_key.key)
        self.assertIsNotNone(self.access_key.created_at)
