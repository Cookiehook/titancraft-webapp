import logging

from django.db import models
from markdownx.models import MarkdownxField

from app.models import constants
from app.models.constants import Enchantment, Potion, ItemIcon
from app.models.locations import Location

logger = logging.getLogger()


class StockRecord(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    cost_item = models.ForeignKey(constants.Item, on_delete=models.CASCADE, related_name="cost")
    cost_stack_size = models.IntegerField()

    units = models.IntegerField()
    last_updated = models.DateTimeField()

    def set_display_data(self, user):
        self.user_is_maintainer = self.location.is_maintainer(user)
        self.item_stacks = []

        for idx, stack in enumerate(self.itemstacktostockrecord_set.all()):
            stack_data = {}
            stack_enchanted = True if stack.enchantmenttoitemstack_set.all() else False
            stack_potion = stack.potiontoitemstack_set.all()[0].potion if stack.potiontoitemstack_set.all() else None

            if stack.stack_size == 64:
                stack_data["stacks"] = 1
                stack_data["items"] = 0
                stack_data['stack_size_label'] = "1 Stack"
            elif stack.stack_size > 64:
                stack_data["stacks"] = int(stack.stack_size / 64)
                stack_data["items"] = 0
                stack_data['stack_size_label'] = f"{stack_data['stacks']} Stacks"
                if stack.stack_size % 64:
                    stack_data["items"] = stack.stack_size % 64
                    stack_data['stack_size_label'] += f" + {stack_data['items']} Items"
            else:
                stack_data["stacks"] = 0
                stack_data["items"] = stack.stack_size
                stack_data['stack_size_label'] = f"{stack.stack_size} Items"

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
    description = MarkdownxField()

    def __str__(self):
        return f"{self.location}: {self.name}"

    def set_display_data(self, user):
        self.user_is_maintainer = self.location.is_maintainer(user)


class FarmRecord(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    mob = models.ForeignKey(constants.Mob, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(constants.Item, on_delete=models.CASCADE, null=True, blank=True)
    xp = models.BooleanField(default=False)

    def __str__(self):
        if self.mob:
            return f"{self.location} - {self.mob} (XP={self.xp})"
        else:
            return f"{self.location} - {self.item}"

    def set_display_data(self, user):
        self.user_is_maintainer = self.location.is_maintainer(user)
        self.view_data = {}
        if self.mob:
            self.view_data['label_type'] = "mob"
            self.view_data['label'] = self.mob.name
            self.view_data['xp'] = self.xp
            self.view_data['icon'] = self.mob.icon
        else:
            self.view_data['label_type'] = "item"
            self.view_data['label'] = self.item.name
            self.view_data['icon'] = ItemIcon.objects.get(item=self.item).icon
