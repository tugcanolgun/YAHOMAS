from django.test import TestCase
from django.db import models
from easy.models import User


class UserTestcase(TestCase):
    def setUp(self):
        User.objects.create(
            username="user",
            password="123123asd"
        )

    def test_user_entities(self):
        """User entity tests"""
        user = User.objects.get(username="user")
        self.assertEqual(user.username, 'user')
        self.assertEqual(user.user_type, 2)
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')