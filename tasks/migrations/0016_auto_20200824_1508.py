# Generated by Django 3.1 on 2020-08-24 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0015_auto_20200821_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklist',
            name='color',
            field=models.CharField(default='#21756b', max_length=30),
        ),
        migrations.AlterField(
            model_name='tasklist',
            name='name',
            field=models.CharField(default='Sans nom', max_length=30, null=True),
        ),
    ]
