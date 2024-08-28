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
