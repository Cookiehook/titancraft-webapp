"""
All data used to create and manage Locations and their stocks.
These are defined by the user.
"""
import logging
import math

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from app.models import constants
from app.models.constants import Enchantment, Potion, ItemIcon

logger = logging.getLogger()


class Location(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    description = models.CharField(max_length=1000, blank=True, null=True)
    x_pos = models.IntegerField(null=True)
    y_pos = models.IntegerField(null=True)
    z_pos = models.IntegerField(null=True)
    region = models.ForeignKey(constants.Region, on_delete=models.CASCADE, null=True)
    spawn_distance = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.name} {self.x_pos}/{self.y_pos}/{self.z_pos} ({self.region})"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # Disregard height when calculating distance to spawn. It's close enough for ordering a web page.
        self.spawn_distance = math.sqrt((self.x_pos * self.x_pos) + (self.z_pos * self.z_pos))
        self.slug = slugify(self.name)
        super(Location, self).save(force_insert, force_update, using, update_fields)


class Maintainer(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.location} - {self.user}"


class StockRecord(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    # Itemstack for sale
    stock_item = models.ForeignKey(constants.Item, on_delete=models.CASCADE, related_name="stock")
    stock_description = models.CharField(max_length=200, null=True, blank=True)
    stock_stack_size = models.IntegerField()

    # Itemstack accepted as payment
    cost_item = models.ForeignKey(constants.Item, on_delete=models.CASCADE, related_name="cost")
    cost_description = models.CharField(max_length=200, null=True, blank=True)
    cost_stack_size = models.IntegerField()

    units = models.IntegerField()
    last_updated = models.DateTimeField()

    def __str__(self):
        return f"{self.location}: {self.stock_stack_size}x {self.stock_item} - {self.cost_stack_size}x {self.cost_item}"
    
    def set_display_data(self):
        stock_enchanted = True if self.enchantmenttostockrecord_set.all() else False
        stock_potion = self.potiontostockrecord_set.all()[0].potion if self.potiontostockrecord_set.all() else None
        if stock_enchanted:
            self.stock_labels = [str(i) for i in self.enchantmenttostockrecord_set.all()]
        elif stock_potion:
            self.stock_labels = [str(i) for i in self.potiontostockrecord_set.all()]
        try:
            self.stock_icon = ItemIcon.objects.get(item=self.stock_item, enchanted=stock_enchanted,
                                                    potion=stock_potion).icon
        except Exception:
            logger.warning(f"Couldn't find icon for {self.stock_item} Enchanted={stock_enchanted} Potion={stock_potion}")
            self.stock_icon = ItemIcon.objects.filter(item=self.stock_item)[0].icon

        try:
            self.cost_icon = ItemIcon.objects.get(item=self.cost_item, enchanted=False, potion=None).icon
        except Exception:
            logger.warning(f"Couldn't find icon for {self.cost_item} Enchanted=None Potion=None")
            self.stock_icon = ItemIcon.objects.filter(item=self.stock_item)[0].icon
    

class EnchantmentToStockRecord(models.Model):
    enchantment = models.ForeignKey(Enchantment, on_delete=models.CASCADE)
    stock_record = models.ForeignKey(StockRecord, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.enchantment}"


class PotionToStockRecord(models.Model):
    potion = models.ForeignKey(Potion, on_delete=models.CASCADE)
    stock_record = models.ForeignKey(StockRecord, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.potion}"


class ServiceRecord(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.location}: {self.name}"


class FarmRecord(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    mob = models.ForeignKey(constants.Mob, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(constants.Item, on_delete=models.CASCADE, null=True, blank=True)
    xp = models.BooleanField(default=False)
