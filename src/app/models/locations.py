"""
All data used to create and manage Locations and their stocks.
These are defined by the user.
"""
import logging
import math

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from markdownx.models import MarkdownxField

from app.models import constants
from app.models.constants import Enchantment, Potion, ItemIcon

logger = logging.getLogger()


class Location(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
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
        self.slug = slugify(self.name)
        super(Location, self).save(force_insert, force_update, using, update_fields)


class Maintainer(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.location} - {self.user}"


class StockRecord(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    cost_item = models.ForeignKey(constants.Item, on_delete=models.CASCADE, related_name="cost")
    cost_stack_size = models.IntegerField()

    units = models.IntegerField()
    last_updated = models.DateTimeField()

    def set_display_data(self, user):
        self.user_is_maintainer = user in [m.user for m in Maintainer.objects.filter(location=self.location)]
        self.item_stacks = []

        for idx, stack in enumerate(self.itemstacktostockrecord_set.all()):
            stack_data = {}
            stack_enchanted = True if stack.enchantmenttoitemstack_set.all() else False
            stack_potion = stack.potiontoitemstack_set.all()[0].potion if stack.potiontoitemstack_set.all() else None

            stack_data['stack_size'] = stack.stack_size
            stack_data['item'] = stack.item.name
            stack_data['description'] = stack.description
            stack_data['final'] = True if idx == len(self.itemstacktostockrecord_set.all()) - 1 else False

            stack_data['label_type'] = "N/A"
            if stack_enchanted:
                stack_data['labels'] = [str(i) for i in stack.enchantmenttoitemstack_set.all()]
                stack_data['label_type'] = "enchantment"
            elif stack_potion:
                stack_data['labels'] = [str(i) for i in stack.potiontoitemstack_set.all()]
                stack_data['label_type'] = "potion"
            try:
                stack_data['icon'] = ItemIcon.objects.get(item=stack.item, enchanted=stack_enchanted, potion=stack_potion).icon
            except Exception:
                logger.warning(f"Couldn't find icon for {stack.item} Enchanted={stack_enchanted} Potion={stack_potion}")
                stack_data['icon'] = ItemIcon.objects.filter(item=stack.item)[0].icon
            self.item_stacks.append(stack_data)

        try:
            self.cost_icon = ItemIcon.objects.get(item=self.cost_item, enchanted=False, potion=None).icon
        except Exception:
            logger.warning(f"Couldn't find icon for {self.cost_item} Enchanted=None Potion=None")
            self.cost_icon = ItemIcon.objects.filter(item=self.cost_item)[0].icon


class ItemStackToStockRecord(models.Model):
    item = models.ForeignKey(constants.Item, on_delete=models.CASCADE, related_name="stock")
    description = models.CharField(max_length=200, null=True, blank=True)
    stack_size = models.IntegerField()
    stock_record = models.ForeignKey(StockRecord, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.stack_size}x {self.item}"


class EnchantmentToItemStack(models.Model):
    enchantment = models.ForeignKey(Enchantment, on_delete=models.CASCADE)
    item_stack = models.ForeignKey(ItemStackToStockRecord, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.enchantment}"


class PotionToItemStack(models.Model):
    potion = models.ForeignKey(Potion, on_delete=models.CASCADE)
    item_stack = models.ForeignKey(ItemStackToStockRecord, on_delete=models.CASCADE)

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
