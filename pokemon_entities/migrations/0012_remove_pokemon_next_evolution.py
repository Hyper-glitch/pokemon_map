# Generated by Django 3.1.14 on 2022-07-04 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0011_auto_20220703_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemon',
            name='next_evolution',
        ),
    ]
