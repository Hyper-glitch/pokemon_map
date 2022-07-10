"""Module for Pokemon and PokemonEntity models."""
from django.db import models  # noqa F401


class PokemonElementType(models.Model):
    """PokemonElementType, M2M related to the Pokemon model."""
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(blank=True, null=True, upload_to='elements', verbose_name='Изображение')

    class Meta:
        verbose_name = "Стихия"
        verbose_name_plural = "Стихии"

    def __str__(self):
        return self.title


class Pokemon(models.Model):
    """Pokemon model."""
    title_ru = models.CharField(max_length=255, verbose_name='Название на русском')
    title_en = models.CharField(max_length=255, blank=True, verbose_name='Название на английском')
    title_jp = models.CharField(max_length=255, blank=True, verbose_name='Название на японском')
    image = models.ImageField(blank=True, null=True, upload_to='pokemons', verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    elements = models.ManyToManyField(PokemonElementType, verbose_name='Стихии')
    previous_evolution = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Из кого эволюционировал', related_name='next_evolutions',
    )

    class Meta:
        verbose_name = "Покемон"
        verbose_name_plural = "Покемоны"

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    """PokemonEntity, related to the Pokemon model."""
    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE, verbose_name='Покемон',
        related_name='entities',
    )
    latitude = models.FloatField(max_length=6, verbose_name=' Широта')
    longitude = models.FloatField(max_length=6, verbose_name=' Долгота')
    appeared_at = models.DateTimeField(verbose_name='Появился в')
    disappeared_at = models.DateTimeField(verbose_name='Исчез в')
    level = models.PositiveSmallIntegerField(verbose_name='Уровень')
    health = models.PositiveSmallIntegerField(verbose_name='Здоровье')
    strength = models.PositiveSmallIntegerField(verbose_name='Атака')
    defence = models.PositiveSmallIntegerField(verbose_name='Защита')
    stamina = models.PositiveSmallIntegerField(verbose_name='Выносливость')

    class Meta:
        verbose_name = "Особь покемона"
        verbose_name_plural = "Особи покемона"

    def __str__(self):
        return self.pokemon.title_ru
