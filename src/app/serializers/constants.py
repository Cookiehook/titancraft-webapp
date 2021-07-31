from rest_framework import serializers

import app.models.constants as models


class BusinessTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BusinessType
        fields = ['id', 'name']


class MobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mob
        fields = ['id', 'name', 'icon']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = ['id', 'name']


class PotionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PotionType
        fields = ['id', 'name']


class PotionModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PotionModifier
        fields = ['id', 'name']


class EnchantmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EnchantmentType
        fields = ['id', 'name']


class EnchantmentLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EnchantmentLevel
        fields = ['id', 'name']


class ItemClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ItemClass
        fields = ['id', 'item', 'name']


class ItemIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ItemIcon
        fields = ['id', 'item', 'enchanted', 'potion', 'icon']
