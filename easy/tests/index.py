from django.test import TestCase, Client
from django.test.utils import setup_test_environment

client = Client()

class IndexViewTests(TestCase):
    def test_home_page_accessable(self):
        response = client.get('/')
        self.assertEqual(response.status_code, 200)


class BookingViewTests(TestCase):
    def test_booking_page_accessable(self):
        response = client.get('/booking/')
        self.assertEqual(response.status_code, 200)


class UserViewTests(TestCase):
    def test_user_page_accessable(self):
        response = client.get('/users/')
        self.assertEqual(response.status_code, 200)


class GuestsViewTests(TestCase):
    def test_booking_page_accessable(self):
        response = client.get('/guest/')
        self.assertEqual(response.status_code, 200)


class RoomViewTests(TestCase):
    def test_booking_page_accessable(self):
        response = client.get('/room/')
        self.assertEqual(response.status_code, 200)
