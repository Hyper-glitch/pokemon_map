# Generated by Django 3.1.14 on 2022-07-10 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0018_auto_20220710_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonelementtype',
            name='strong_against',
            field=models.ManyToManyField(blank=True, null=True, to='pokemon_entities.PokemonElementType', verbose_name='Силён против'),
        ),
    ]
