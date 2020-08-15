from accounts.forms import UserRegisterForm, UserLoginForm
from django.test import TestCase, Client
from django.contrib.auth.models import User


class AccountsFormsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_valid_data(self):
        form = UserRegisterForm(data={
            'email': 'thetest@test.com',
            'pw1': 'testtest',
            'pw2': 'testtest'
        })

        self.assertTrue(form.is_valid())

    def test_register_form_not_valid_if_no_data(self):
        form = UserRegisterForm(data={})

        self.assertFalse(form.is_valid())

    def test_login_valid_data(self):

        User.objects.create_user(username='thetest@test.com',
                                 email='thetest@test.com',
                                 password='testtest')

        form = UserLoginForm(data={
            'username': 'thetest@test.com',
            'password': 'testtest',
        })

        self.assertTrue(form.is_valid())

    def test_login_form_not_valid_if_no_data(self):
        form = UserLoginForm(data={})

        self.assertFalse(form.is_valid())
