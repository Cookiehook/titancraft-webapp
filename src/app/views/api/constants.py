from rest_framework import viewsets

import app.models.constants as models
import app.serializers.constants as serializers
from app import permissions


class BusinessTypeViewSet(viewsets.ModelViewSet):
    queryset = models.BusinessType.objects.all().order_by('name')
    serializer_class = serializers.BusinessTypeSerializer
    permission_classes = [permissions.IsSiteAdminOrReadOnly]


class DimensionViewSet(viewsets.ModelViewSet):
    queryset = models.Dimension.objects.all().order_by('name')
    serializer_class = serializers.DimensionSerializer
    permission_classes = [permissions.IsSiteAdminOrReadOnly]


class MobViewSet(viewsets.ModelViewSet):
    queryset = models.Mob.objects.all().order_by('name')
    serializer_class = serializers.MobSerializer
    permission_classes = [permissions.IsSiteAdminOrReadOnly]


class ItemViewSet(viewsets.ModelViewSet):
    queryset = models.Item.objects.all().order_by('name')
    serializer_class = serializers.ItemSerializer
    permission_classes = [permissions.IsSiteAdminOrReadOnly]


class PotionTypeViewSet(viewsets.ModelViewSet):
    queryset = models.PotionType.objects.all().order_by('name')
    serializer_class = serializers.PotionTypeSerializer
    permission_classes = [permissions.IsSiteAdminOrReadOnly]


class PotionModifierViewSet(viewsets.ModelViewSet):
    queryset = models.PotionModifier.objects.all().order_by('name')
    serializer_class = serializers.PotionModifierSerializer
    permission_classes = [permissions.IsSiteAdminOrReadOnly]


class EnchantmentTypeViewSet(viewsets.ModelViewSet):
    queryset = models.EnchantmentType.objects.all().order_by('name')
    serializer_class = serializers.EnchantmentTypeSerializer
    permission_classes = [permissions.IsSiteAdminOrReadOnly]


class EnchantmentLevelViewSet(viewsets.ModelViewSet):
    queryset = models.EnchantmentLevel.objects.all().order_by('name')
    serializer_class = serializers.EnchantmentLevelSerializer
    permission_classes = [permissions.IsSiteAdminOrReadOnly]


class ItemClassViewSet(viewsets.ModelViewSet):
    queryset = models.ItemClass.objects.all().order_by('item')
    serializer_class = serializers.ItemClassSerializer
    permission_classes = [permissions.IsSiteAdminOrReadOnly]


class ItemIconViewSet(viewsets.ModelViewSet):
    queryset = models.ItemIcon.objects.all().order_by('item')
    serializer_class = serializers.ItemIconSerializer
    permission_classes = [permissions.IsSiteAdminOrReadOnly]
