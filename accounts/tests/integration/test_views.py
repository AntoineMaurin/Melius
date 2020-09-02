from django.test import TestCase, Client
from django.contrib.auth.models import User
from accounts.forms import UserRegisterForm, UserLoginForm
from django.contrib import auth
from tasks.models import TaskList


class AccountsViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login_get(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.failUnless(isinstance(response.context['form'], UserLoginForm))

    def test_register_get(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.failUnless(isinstance(response.context['form'], UserRegisterForm))

    def test_logout_get(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login')

    def test_register_success(self):
        response = self.client.post('/register', {
            'email': 'thetest@test.com',
            'pw1': 'testtest',
            'pw2': 'testtest'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        self.assertRedirects(response, '/login')

    def test_register_fails(self):
        response = self.client.post('/register', {
            'email': 'anothertest@test.com',
            'pw1': 'testtest',
            'pw2': 'wrongconfirm'
        })

        self.assertEquals(response.status_code, 200)
        self.assertEquals(User.objects.count(), 0)
        self.assertTemplateUsed(response, 'register.html')
        self.failUnless(isinstance(response.context['form'], UserRegisterForm))

    def test_login_success_post(self):

        user = User.objects.create_user(username='test@test.com',
                                        email='test@test.com',
                                        password='testtest')

        response = self.client.post('/login', {
            'username': 'test@test.com',
            'password': 'testtest'
        })

        TaskList.objects.create(user=user)
        #
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/dashboard')

        user = auth.get_user(self.client)
        self.assertEquals(user.is_authenticated, True)

    def test_login_fails(self):
        user = User.objects.create_user(username='test@test.com',
                                        email='test@test.com',
                                        password='testtest')

        response = self.client.post('/login', {
            'username': 'test@test.com',
            'password': 'wrongpassword'
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        """Creates account, connect, and disconnect to check the efficiency of
        the logout view"""

        user = User.objects.create_user(username='test@test.com',
                                        email='test@test.com',
                                        password='testtest')

        TaskList.objects.create(user=user)

        self.client.post('/login', {
            'username': 'test@test.com',
            'password': 'testtest'
        })

        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

        response = self.client.get('/logout')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login')

        disconnected_user = auth.get_user(self.client)
        self.assertFalse(disconnected_user.is_authenticated)
