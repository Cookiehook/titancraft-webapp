from rest_framework import viewsets, permissions

import app.models.itemstacks as models
import app.serializers.itemstacks as serializers


class EnchantmentViewSet(viewsets.ModelViewSet):
    queryset = models.Enchantment.objects.all().order_by('enchantment_type')
    serializer_class = serializers.EnchantmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class PotionViewSet(viewsets.ModelViewSet):
    queryset = models.Potion.objects.all().order_by('potion_type')
    serializer_class = serializers.PotionSerializer
    permission_classes = [permissions.IsAuthenticated]


class PotionModifierToPotionViewSet(viewsets.ModelViewSet):
    queryset = models.PotionModifierToPotion.objects.all().order_by('potion_modifier')
    serializer_class = serializers.PotionModifierToPotionSerializer
    permission_classes = [permissions.IsAuthenticated]
