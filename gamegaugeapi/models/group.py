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

        common_games = Game.objects.annotate(
            num_owners=Count("usergame", filter=Q(usergame__user__in=self.members.all()))
        ).filter(
            num_owners=member_count,
            max_players__gte=member_count
        )

        return common_games