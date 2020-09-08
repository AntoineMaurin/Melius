Projet 13 - Melius

# Présentation

Melius est une application de gestion de tâches qui met à disposition plusieurs méthodologies d'organisation.
Vous pouvez créer / éditer / supprimer des tâches, définir une date limite, ajouter une description, ou encore préciser si votre tâche est urgente et / ou importante.
Vous pouvez aussi manipuler des catégories de tâches, les éditer et les supprimer.
Vos tâches apparaissent ensuite dans les méthodologies implémentées pour le moment :

- Matrice de Stephen Covey (rapport urgence / importance des tâches)
- Kanban personnel (vision en flux)

Et à venir : 

- Time blocking (bloquage d'agenda)
- Pomodoro (sessions de travail mesurées)

Ces méthodologies n'étant pas forcément connues, il est prévu d'ajouter des sections sous chaque page dédiée à une méthodologie expliquant en quoi elle consiste, et quelques conseils pour bien l'utiliser.
Il est également prévu d'ajouter à l'avenir la possibilité de créer des tâches récurrentes.

# Installation

Si vous êtes simple utilisateur, vous pouvez vous rendre sur le site du projet à l'adresse suivante : https://melius.herokuapp.com/

Si vous voulez installer le projet chez vous, il vous faut python (version 3.6.5):

https://www.python.org/downloads/

Une fois installé, forkez ce repo dans votre espace github (bouton fork en haut à droite), puis clonez le sur votre machine à l'aide du bouton vert "Clone".

Maintenant, le projet est sur votre ordinateur, vous devez installer les dépendances pour le faire fonctionner.
Pour cela, il vous faut un gestionnaire de paquets, tel que pip : https://pip.pypa.io/en/stable/installing/

Ouvrez un terminal et rendez-vous dans votre dossier d'installation, à l'endroit où se trouve le fichier "requirements.txt".
Une fois au bon endroit, lancez la commande :
```pip install -r requirements.txt```
Cela installe les dépendances dont le projet a besoin pour fonctionner.

Vous devez également créer votre base de données postgresql ou en utiliser une existante.
Pour installer Postgres : https://www.postgresql.org/
Vous devrez ensuite renseigner les informations de connexion à votre base dans le fichier Melius/settings.py dans la section DATABASES:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Nom de votre base de données',
        'USER': 'Nom de votre utilisateur',
        'PASSWORD': 'Votre mot de passe',
        'HOST': 'Votre hôte',
        'PORT': 'Votre port de connexion',
    }
}
```

Maintenant, vous devez créer les tables de la base de données avant de la remplir :
Lancez les commandes :

```python manage.py makemigrations```

```python manage.py migrate```

Une fois terminé,vous n'avez plus qu'à lancer le serveur de développement :
```python manage.py runserver```

Vous pouvez désormais utiliser le projet en local, généralement à l'adresse ```127.0.0.1:8000```

Le projet contient des tests, pour les lancer, utilisez la commande ```python manage.py test```
