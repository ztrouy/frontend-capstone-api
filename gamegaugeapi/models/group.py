from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(
        "User",
        through="UserGroup",
        related_name="groups"
    )


    def __str__(self):
        return self.name