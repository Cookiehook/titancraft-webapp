from rest_framework import serializers

import app.models.itemstacks as models


class EnchantmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Enchantment
        fields = ['id', 'stock_record', 'enchantment_type', 'enchantment_level']


class PotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Potion
        fields = ['id', 'stock_record', 'potion_type']


class PotionModifierToPotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PotionModifierToPotion
        fields = ['id', 'potion', 'potion_modifier']
