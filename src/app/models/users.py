from django.contrib.auth.models import User
from django.db import models


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    discord_id = models.CharField(max_length=200)
    avatar_hash = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.user}"
