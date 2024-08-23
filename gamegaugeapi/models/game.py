from django.db import models
from .platform import Platform
from django.core.validators import MinValueValidator


class Game(models.Model):
    name = models.CharField(max_length=260)
    max_players = models.IntegerField(validators=[MinValueValidator(1)])
    image_header = models.URLField()
    genres = models.ManyToManyField(
        "Genre",
        through="GameGenre",
        related_name="games"
    )
    platforms = models.ManyToManyField(
        "Platform",
        through="GamePlatform",
        related_name="games"
    )


    def __str__(self):
        return self.name