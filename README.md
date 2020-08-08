Projet 13 - Melius

# Présentation

Ce projet est le projet final d'une formation Python.

# Fonctionnement


# Utilisation


# Installation

Si vous êtes simple utilisateur, vous pouvez vous rendre sur le site du projet à l'adresse suivante :

Si vous voulez installer le projet chez vous, il vous faut python (version 3.6.5):

https://www.python.org/downloads/

Une fois installé, forkez ce repo dans votre espace github (bouton fork en haut à droite), puis clonez le sur votre machine à l'aide du bouton vert "Clone".

Maintenant, le projet est sur votre ordinateur, vous devez installer les dépendances pour le faire fonctionner.
Pour cela, il vous faut un gestionnaire de paquets, tel que pip : https://pip.pypa.io/en/stable/installing/

Ouvrez un terminal si ce n'est pas déjà fait et rendez-vous dans votre dossier d'installation, à l'endroit où se trouve le fichier "requirements.txt".
Une fois au bon endroit, lancez la commande :
```pip install -r requirements.txt```
Cela installe les dépendances dont le projet a besoin pour fonctionner.

Vous devez également créer votre base de données postgresql ou en utiliser une existante.

Maintenant, vous devez créer les tables de la base de données avant de la remplir :
Lancez les commandes :

```python manage.py makemigrations```

```python manage.py migrate```

Une fois terminé,vous n'avez plus qu'à lancer le serveur de développement :
```python manage.py runserver```

Vous pouvez désormais utiliser le projet en local, généralement à l'adresse ```127.0.0.1:8000```

Une dernière chose, le projet contient des tests, pour les lancer, utilisez la commande ```python manage.py test```

Sachez par contre qu'il y a un test selenium, qui est effectué sur chrome, donc vous devez installer le chrome driver de votre version de chrome pour que ce test soit fonctionnel. Vous pouvez télécharger le ChromeDriver via ce lien : https://chromedriver.chromium.org/downloads,
et placer l'executable dans ```melius\tests\functionnal```
