# Generated by Django 3.1 on 2020-08-21 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0014_tasklist_couleur'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tasklist',
            old_name='couleur',
            new_name='color',
        ),
    ]