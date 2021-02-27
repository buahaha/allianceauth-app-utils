from django.test import TestCase

import requests
from django.contrib.auth.models import User

from app_utils.testing import NoSocketsTestCase, SocketAccessError, generate_invalid_pk


class TestNoSocketsTestCase(NoSocketsTestCase):
    def test_raises_exception_on_attempted_network_access(self):

        with self.assertRaises(SocketAccessError):
            requests.get("https://www.google.com")


class TestGenerateInvalidPk(TestCase):
    def test_normal(self):
        User.objects.all().delete()
        User.objects.create(username="John Doe", password="dummy")
        invalid_pk = generate_invalid_pk(User)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=invalid_pk)
