# Generated by Django 3.1.14 on 2022-07-12 19:56

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0019_pokemonelementtype_strong_against'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='pokemonentity',
            managers=[
                ('pokemons', django.db.models.manager.Manager()),
            ],
        ),
    ]
