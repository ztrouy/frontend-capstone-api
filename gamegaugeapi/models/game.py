from django.db import models
from django.contrib.auth.models import User
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
    owners = models.ManyToManyField(
        User,
        through="UserGame",
        related_name="games"
    )


    def __str__(self):
        return self.name