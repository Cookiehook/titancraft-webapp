"""
Relational tables required to mimic the structures used to make the in-game ItemStack.
An ItemStack is comprised of:
    - 1 to 1 Item
    - 1 to 0|Many Potion (1 PotionType & 0|Many PotionModifiers)
    - 1 to 0|Many Enchantments (1 EnchantmentType & 1 EnchantmentLevel)
Each ItemStack is associated with a StockRecord, which details the price and availability.

None of these classes are made visible to the user. They only exist to satisfy the relationships required to
manage stock records.
"""
from django.db import models

from app.models import constants


class ItemStack(models.Model):
    item = models.ForeignKey(constants.Item, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, null=True, blank=True)
    stack_size = models.IntegerField()

    def __str__(self):
        if enchantments := EnchantmentToItemStack.objects.filter(item_stack=self):
            enchantment_labels = [str(e.enchantment) for e in enchantments]
            return f"{self.stack_size}x {self.item} ({'|'.join(enchantment_labels)})"
        if potions := PotionToItemStack.objects.filter(item_stack=self):
            potion_labels = [str(p.potion) for p in potions]
            return f"{self.stack_size}x {self.item} ({'|'.join(potion_labels)})"
        return f"{self.stack_size}x {self.item}"


class Enchantment(models.Model):
    enchantment_type = models.ForeignKey(constants.EnchantmentType, on_delete=models.CASCADE)
    enchantment_level = models.ForeignKey(constants.EnchantmentLevel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.enchantment_type} - {self.enchantment_level}"


class Potion(models.Model):
    potion_type = models.ForeignKey(constants.PotionType, on_delete=models.CASCADE)

    def __str__(self):
        if modifiers := PotionModifierToPotion.objects.filter(potion=self):
            modifier_labels = [str(m.potion_modifier) for m in modifiers]
            return f"{self.potion_type} ({'|'.join(modifier_labels)})"

        return f"{self.potion_type}"


class PotionModifierToPotion(models.Model):
    potion_modifier = models.ForeignKey(constants.PotionModifier, on_delete=models.CASCADE)
    potion = models.ForeignKey(Potion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.potion} - {self.potion_modifier}"


class EnchantmentToItemStack(models.Model):
    enchantment = models.ForeignKey(Enchantment, on_delete=models.CASCADE)
    item_stack = models.ForeignKey(ItemStack, on_delete=models.CASCADE)


class PotionToItemStack(models.Model):
    potion = models.ForeignKey(Potion, on_delete=models.CASCADE)
    item_stack = models.ForeignKey(ItemStack, on_delete=models.CASCADE)
