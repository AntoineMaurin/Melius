# Generated by Django 3.1 on 2020-08-20 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0011_simpletask_due_date_clean_display'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklist',
            name='name',
            field=models.CharField(default=None, max_length=25, null=True),
        ),
    ]
