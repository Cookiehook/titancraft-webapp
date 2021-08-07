"""
All data used to create and manage Locations and their stocks.
These are defined by the user.
"""
import logging
import math

from django.contrib.auth.models import User
from django.db import models
from markdownx.models import MarkdownxField

from app.models import constants

logger = logging.getLogger()


class Location(models.Model):
    name = models.CharField(max_length=200)
    description = MarkdownxField(null=True)
    x_pos = models.IntegerField(default=0)
    y_pos = models.IntegerField(default=0)
    z_pos = models.IntegerField(default=0)
    region = models.ForeignKey(constants.Region, on_delete=models.CASCADE, null=True)
    spawn_distance = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.name} {self.x_pos}/{self.y_pos}/{self.z_pos} ({self.region})"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # Disregard height when calculating distance to spawn. It's close enough for ordering a web page.
        self.spawn_distance = math.sqrt((self.x_pos * self.x_pos) + (self.z_pos * self.z_pos))
        super(Location, self).save(force_insert, force_update, using, update_fields)

    def set_display_data(self, user):
        self.user_is_maintainer = self.is_maintainer(user)

    def is_maintainer(self, user):
        maintainers = Maintainer.objects.filter(location=self)
        return user.is_staff or user in [m.user for m in maintainers]

    def set_player_distance(self, x_pos, z_pos):
        self.player_distance = math.sqrt((self.x_pos - x_pos)*(self.x_pos - x_pos) +
                                         (self.z_pos - z_pos)*(self.z_pos - z_pos))


class Maintainer(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.location} - {self.user}"
