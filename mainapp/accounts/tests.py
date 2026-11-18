from django.test import TestCase
from django.urls import reverse


class AccountsUrlTests(TestCase):
    def test_signup_page_loads(self):
        response = self.client.get(reverse("signup"), {"role": "doctor"})
        self.assertEqual(response.status_code, 200)
