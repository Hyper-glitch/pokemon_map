from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True, upload_to='pokemons')

    def __str__(self):
        return self.title


class PokemonGeo(models.Model):
    latitude = models.FloatField(max_length=6, verbose_name=' Широта')
    longitude = models.FloatField(max_length=6, verbose_name=' Долгота')
