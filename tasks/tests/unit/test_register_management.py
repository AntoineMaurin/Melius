from django.test import TestCase
from accounts.register_management import RegisterManagement
from django.contrib.auth.models import User


class RegisterManagementTest(TestCase):

    def test_email_already_used(self):
        User.objects.create_user(username='test@test.com',
                                 email='test@test.com',
                                 password='testtest')
        data = {
            'email': 'test@test.com',
            'pw1': 'testtest',
            'pw2': 'testtest'
        }
        rm = RegisterManagement(email=data['email'],
                                pw1=data['pw1'],
                                pw2=data['pw2'])
        response = rm.analyze()
        self.assertEquals(response[0], 'error')
        self.assertEquals(response[1], 'Cet email est déjà utilisé')

    def test_passwords_not_matching(self):
        data = {
            'email': 'test@test.com',
            'pw1': 'testtest',
            'pw2': 'wrongconfirm'
        }
        rm = RegisterManagement(email=data['email'],
                                pw1=data['pw1'],
                                pw2=data['pw2'])
        resp = rm.analyze()
        self.assertEquals(resp[0], 'error')
        self.assertEquals(resp[1], 'Les mots de passe ne correspondent pas')

    def test_password_too_short(self):
        data = {
            'email': 'test@test.com',
            'pw1': 'short',
            'pw2': 'short'
        }
        rm = RegisterManagement(email=data['email'],
                                pw1=data['pw1'],
                                pw2=data['pw2'])
        response = rm.analyze()
        self.assertEquals(response[0], 'error')
        self.assertEquals(response[1], ("Ce mot de passe est trop court, il do"
                                        "it comporter au moins 6 caractères."))

    def test_invalid_email(self):
        data = {
            'email': 'testtest.com',
            'pw1': 'testtest',
            'pw2': 'testtest'
        }
        rm = RegisterManagement(email=data['email'],
                                pw1=data['pw1'],
                                pw2=data['pw2'])
        response = rm.analyze()
        self.assertEquals(response[0], 'error')
        self.assertEquals(response[1], "Email invalide")

    def test_no_email(self):
        data = {
            'email': '',
            'pw1': 'testtest',
            'pw2': 'testtest'
        }
        rm = RegisterManagement(email=data['email'],
                                pw1=data['pw1'],
                                pw2=data['pw2'])
        response = rm.analyze()
        self.assertEquals(response[0], 'error')
        self.assertEquals(response[1], "Email invalide")

    def test_success(self):
        data = {
            'email': 'test@test.com',
            'pw1': 'testtest',
            'pw2': 'testtest'
        }
        rm = RegisterManagement(email=data['email'],
                                pw1=data['pw1'],
                                pw2=data['pw2'])
        r = rm.analyze()
        self.assertEquals(r[0], 'success')
        self.assertEquals(r[1], "Compte créé ! Bienvenue " + data['email'])
