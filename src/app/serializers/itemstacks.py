from rest_framework import serializers

import app.models.itemstacks as models


class ItemStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ItemStack
        fields = ['id', 'item', 'description', 'stack_size']


class EnchantmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Enchantment
        fields = ['id', 'enchantment_type', 'enchantment_level']


class PotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Potion
        fields = ['id', 'potion_type']


class PotionModifierToPotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PotionModifierToPotion
        fields = ['id', 'potion', 'potion_modifier']


class EnchantmentToItemStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EnchantmentToItemStack
        fields = ['id', 'enchantment', 'item_stack']


class PotionToItemStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PotionToItemStack
        fields = ['id', 'potion', 'item_stack']
