from django.contrib.auth.models import User
from validate_email import validate_email


class RegisterManagement:

    def __init__(self, email=None, pw1=None, pw2=None):
        self.email = email
        self.pw1 = pw1
        self.pw2 = pw2

    def analyze(self):
        if User.objects.filter(email=self.email).exists():
            return ('error', 'Cet email est déjà utilisé')
        elif self.pw1 != self.pw2:
            return ('error', 'Les mots de passe ne correspondent pas')
        elif len(self.pw1) < 6:
            return ('error', "Ce mot de passe est trop court, "
                    "il doit comporter au moins 6 caractères.")
        elif not validate_email(self.email):
            return ('error', "Email invalide")
        else:
            return ('success', 'Compte créé ! Bienvenue ' + self.email)
