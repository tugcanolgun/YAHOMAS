from django.test import TestCase
from django.db import models
from easy.models import Guests

class GuestTestcase(TestCase):
    def setUp(self):
        Guests.objects.create(name="Name", surname="Surname")

    def test_user_entities(self):
        """Animals that can speak are correctly identified"""
        user1 = Guests.objects.get(name="Name")
        self.assertEqual(user1.name, 'Name')
        self.assertEqual(user1.surname, 'Surname')
        self.assertEqual(user1.image.name, '')
