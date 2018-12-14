from django.test import TestCase, Client
from django.test.utils import setup_test_environment

client = Client()

class IndexViewTests(TestCase):
    def test_home_page_accessable(self):
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
