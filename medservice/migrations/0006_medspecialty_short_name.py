# Generated by Django 4.2.1 on 2023-05-28 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medservice', '0005_remove_medspecialty_short_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='medspecialty',
            name='short_name',
            field=models.CharField(default='hju', max_length=10),
        ),
    ]
