# Generated by Django 3.1 on 2020-08-31 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0017_auto_20200827_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='simpletask',
            name='in_progress',
            field=models.BooleanField(default=False),
        ),
    ]
