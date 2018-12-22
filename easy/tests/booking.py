from django.test import TestCase
from django.db import models
from easy.models import Guests

class GuestTestcase(TestCase):
    def setUp(self):
        Guests.objects.create(name="Name", surname="Surname")
        Guests.objects.create(name="Trial",
            surname="Surname",
            phone="010101",
            id_number="123123",
            )

    def test_guest_entities(self):
        """Booking entity test"""
        user1 = Guests.objects.get(name="Name")
        user2 = Guests.objects.get(name="Trial")
        self.assertEqual(user1.name, 'Name')
        self.assertEqual(user1.surname, 'Surname')
        self.assertEqual(user1.image.name, '')
        
        self.assertEqual(user2.name, 'Trial')
        self.assertEqual(user2.surname, 'Surname')
        self.assertEqual(user2.phone, '010101')
        self.assertEqual(user2.id_number, '123123')

