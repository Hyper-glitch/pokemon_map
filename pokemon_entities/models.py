from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True, upload_to='pokemons')

    class Meta:
        verbose_name = "Покемон"
        verbose_name_plural = "Покемоны"

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')
    latitude = models.FloatField(max_length=6, verbose_name=' Широта')
    longitude = models.FloatField(max_length=6, verbose_name=' Долгота')
    appeared_at = models.DateTimeField(verbose_name='Появился в')
    disappeared_at = models.DateTimeField(verbose_name='Исчез в')
    level = models.PositiveSmallIntegerField(default=1, verbose_name='Уровень')
    health = models.PositiveSmallIntegerField(default=100, verbose_name='Здоровье')
    strength = models.PositiveSmallIntegerField(default=10, verbose_name='Атака')
    defence = models.PositiveSmallIntegerField(default=10, verbose_name='Защита')
    stamina = models.PositiveSmallIntegerField(default=10, verbose_name='Выносливость')

    class Meta:
        verbose_name = "Особь покемона"
        verbose_name_plural = "Особи покемона"

    def __str__(self):
        return self.pokemon.title
