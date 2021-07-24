"""
All data to be used as constants by higher models.
These will generally be created once on project release, and maintained as Minecraft or Titancraft receives updates.
"""
from django.db import models


class BusinessType(models.Model):  # eg: Shop, Farm
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):  # eg: diamond_sword
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class EnchantmentLevel(models.Model):  # eg: I, II, III, IV, V
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class EnchantmentType(models.Model):  # eg: Efficiency, Protection
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class PotionModifier(models.Model):  # eg: Strong, Extended, Splash, Lingering
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class PotionType(models.Model):  # eg: Regeneration, Night Vision
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class ItemClass(models.Model):
    # Classifiers to assist in searching eg: Acacia Button is in the "Wood" and "Redstone" class
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.item} - {self.name}"


class ItemIcon(models.Model):  # Find appropriate icon based on Item and modifiers
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    enchanted = models.BooleanField(default=False)
    potion = models.ForeignKey(PotionType, on_delete=models.CASCADE, blank=True, null=True)
    icon = models.CharField(max_length=200)

    def __str__(self):
        if self.enchanted:
            return f"{self.item} (Enchanted)"
        elif self.potion is not None:
            return f"{self.item} ({self.potion})"
        return self.item
