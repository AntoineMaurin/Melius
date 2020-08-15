from django.urls import reverse, resolve
from django.test import TestCase
from accounts.views import register, user_login, user_logout


class AccountsUrlsTest(TestCase):

    def test_register_url_is_resolved(self):
        url = reverse(register)
        self.assertEqual(resolve(url).func, register)

    def test_login_url_is_resolved(self):
        url = reverse(user_login)
        self.assertEqual(resolve(url).func, user_login)

    def test_logout_url_is_resolved(self):
        url = reverse(user_logout)
        self.assertEqual(resolve(url).func, user_logout)
