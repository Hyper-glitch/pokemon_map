"""Module for Pokemon and PokemonEntity models."""
from django.db import models  # noqa F401


class Pokemon(models.Model):
    """Pokemon model."""
    title_ru = models.CharField(max_length=255, verbose_name='Название на русском')
    title_en = models.CharField(max_length=255, blank=True, verbose_name='Название на английском')
    title_jp = models.CharField(max_length=255, blank=True, verbose_name='Название на японском')
    image = models.ImageField(blank=True, null=True, upload_to='pokemons', verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Из кого эволюционировал', related_name='pokemon_previous_evolution',
    )

    class Meta:
        verbose_name = "Покемон"
        verbose_name_plural = "Покемоны"

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    """PokemonEntity, related to the Pokemon model."""
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')
    latitude = models.FloatField(max_length=6, verbose_name=' Широта')
    longitude = models.FloatField(max_length=6, verbose_name=' Долгота')
    appeared_at = models.DateTimeField(verbose_name='Появился в')
    disappeared_at = models.DateTimeField(verbose_name='Исчез в')
    level = models.PositiveSmallIntegerField(default=1, verbose_name='Уровень', blank=True)
    health = models.PositiveSmallIntegerField(default=100, verbose_name='Здоровье', blank=True)
    strength = models.PositiveSmallIntegerField(default=10, verbose_name='Атака', blank=True)
    defence = models.PositiveSmallIntegerField(default=10, verbose_name='Защита', blank=True)
    stamina = models.PositiveSmallIntegerField(default=10, verbose_name='Выносливость', blank=True)

    class Meta:
        verbose_name = "Особь покемона"
        verbose_name_plural = "Особи покемона"

    def __str__(self):
        return self.pokemon.title_ru
