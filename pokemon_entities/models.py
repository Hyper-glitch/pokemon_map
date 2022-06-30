from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True, upload_to='pokemons')

    def __str__(self):
        return self.title
