import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse

from app.models.constants import BusinessType, EnchantmentLevel, EnchantmentType, \
    PotionModifier, PotionType, Item, ItemIcon, ItemClass


@login_required()
def initialise(request):
    if not request.user.is_staff:
        return HttpResponseForbidden(b'Only staff may use this endpoint')

    with open("base_data.json") as datafile:
        base_data = json.loads(datafile.read())

    for obj in base_data['business_types']:
        BusinessType.objects.get_or_create(**obj)

    for obj in base_data['enchantment_levels']:
        EnchantmentLevel.objects.get_or_create(**obj)

    for obj in base_data['enchantment_types']:
        EnchantmentType.objects.get_or_create(**obj)

    for obj in base_data['potion_modifiers']:
        PotionModifier.objects.get_or_create(**obj)

    for obj in base_data['potion_types']:
        PotionType.objects.get_or_create(**obj)

    for obj in base_data['items']:
        potion = None
        if "potion" in obj:
            potion = PotionType.objects.get(name=obj["potion"])

        item, _ = Item.objects.get_or_create(name=obj['name'])

        ItemIcon.objects.get_or_create(item=item,
                                       enchanted=obj.get("enchanted", False),
                                       potion=potion,
                                       icon=obj["icon"]
                                       )
        for item_class in obj.get("classes", []):
            ItemClass.objects.get_or_create(item=item, name=item_class)

    return redirect(reverse('index'))
