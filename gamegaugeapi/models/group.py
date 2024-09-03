from django.db import models
from django.db.models import Count, Q
from django.contrib.auth.models import User
from .game import Game


class Group(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(
        User,
        through="UserGroup",
        related_name="joined_groups"
    )


    def __str__(self):
        return self.name


    def get_common_games(self):
        member_count = self.members.count()

        if member_count == 0:
            return Game.objects.none()

        common_games = set(self.members.first().games.all())

        for member in self.members.all()[1:]:
            common_games = common_games.intersection(set(member.games.all()))

        common_games = Game.objects.filter(
            id__in=[game.id for game in common_games],
            max_players__gte=member_count
        )

        return common_games