# Generated by Django 4.2.1 on 2023-05-28 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medservice', '0004_medspecialty_short_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medspecialty',
            name='short_name',
        ),
    ]
