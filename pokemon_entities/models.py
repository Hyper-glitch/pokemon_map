"""Module for Pokemon and PokemonEntity models."""
from django.db import models  # noqa F401
from django.db.models import Q
from django.utils import timezone


class PokemonElementType(models.Model):
    """PokemonElementType, M2M related to the Pokemon model."""
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(blank=True, null=True, upload_to='elements', verbose_name='Изображение')
    strong_against = models.ManyToManyField(
        'self', null=True, blank=True, symmetrical=False, verbose_name='Силён против',
    )

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


class PokemonEntityQuerySet(models.QuerySet):
    """PokemonEntityQuerySet."""
    def on_map(self, pokemon_id=None, show_all=None):
        """
        Filter pokemon's entities from database in order to appeared and disappeared time. Also could show all pokemons.
        :param pokemon_id: id of a pokemon obj.
        :param show_all: flag that control to render all pokemons or one entity.
        :return: all_entities: filtered entities queryset.
        """
        now = timezone.localtime()
        all_entities = self.filter(Q(appeared_at__lt=now) & Q(disappeared_at__gt=now))
        if not show_all:
            all_entities = all_entities.filter(pokemon__id=pokemon_id)
        return all_entities


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
    pokemons = PokemonEntityQuerySet.as_manager()

    class Meta:
        verbose_name = "Особь покемона"
        verbose_name_plural = "Особи покемона"

    def __str__(self):
        return self.pokemon.title_ru
