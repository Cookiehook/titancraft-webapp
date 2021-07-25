"""
Relational tables required to mimic the structures used to make the in-game ItemStack.
An ItemStack is comprised of:
    - 1 to 1 Item
    - Count of Items (usually 1-64)
    - 1 to 0|Many Potion (1 PotionType & 0|Many PotionModifiers)
    - 1 to 0|Many Enchantments (1 EnchantmentType & 1 EnchantmentLevel)
Each StockRecord has fields representing an ItemStack for the sold item, and accepted payment.
For ease of implementation, only the stock stack can have enchantments and potions added. In the rare
case a user wants to request a stocked / enchanted item as payment, they can still use the description textfield

None of these classes are made directly visible to the user. They only exist to satisfy the relationships required to
manage stock records.
"""
from django.db import models

from app.models import constants, businesses


class Enchantment(models.Model):
    stock_record = models.ForeignKey(businesses.StockRecord, on_delete=models.CASCADE)
    enchantment_type = models.ForeignKey(constants.EnchantmentType, on_delete=models.CASCADE)
    enchantment_level = models.ForeignKey(constants.EnchantmentLevel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.enchantment_type} - {self.enchantment_level}"


class Potion(models.Model):
    stock_record = models.ForeignKey(businesses.StockRecord, on_delete=models.CASCADE)
    potion_type = models.ForeignKey(constants.PotionType, on_delete=models.CASCADE)

    def __str__(self):
        if modifiers := PotionModifierToPotion.objects.filter(potion=self):
            modifier_labels = [str(m.potion_modifier) for m in modifiers]
            return f"{self.potion_type} ({' | '.join(modifier_labels)})"

        return f"{self.potion_type}"


class PotionModifierToPotion(models.Model):
    potion_modifier = models.ForeignKey(constants.PotionModifier, on_delete=models.CASCADE)
    potion = models.ForeignKey(Potion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.potion} - {self.potion_modifier}"
