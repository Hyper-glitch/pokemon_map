# Generated by Django 3.1.14 on 2022-07-01 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0006_auto_20220701_1231'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pokemon',
            options={'verbose_name': 'Покемон', 'verbose_name_plural': 'Покемоны'},
        ),
        migrations.AlterModelOptions(
            name='pokemonentity',
            options={'verbose_name': 'Особь покемона', 'verbose_name_plural': 'Особи покемона'},
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='pokemons', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
    ]
