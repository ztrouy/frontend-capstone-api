from django.db import models
from .game import Game
from .format import Format


class GameFormat(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    format = models.ForeignKey(Format, on_delete=models.CASCADE)