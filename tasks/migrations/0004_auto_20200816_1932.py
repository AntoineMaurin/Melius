# Generated by Django 3.1 on 2020-08-16 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20200816_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simpletask',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='simpletask',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]