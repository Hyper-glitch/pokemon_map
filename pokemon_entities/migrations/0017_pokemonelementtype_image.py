# Generated by Django 3.1.14 on 2022-07-10 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0016_auto_20220709_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonelementtype',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='elements', verbose_name='Изображение'),
        ),
    ]