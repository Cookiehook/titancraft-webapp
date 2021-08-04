import datetime
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse

from app.models.constants import Region, Enchantment, Potion, Item, ItemIcon, ItemClass, Mob
from app.models.locations import Location, Maintainer, StockRecord, EnchantmentToItemStack, PotionToItemStack
from app.models.users import UserDetails


@login_required()
def initialise(request):
    if not request.user.is_staff:
        return HttpResponseForbidden(b'Only staff may use this endpoint')

    with open("reference_data.json") as datafile:
        reference_data = json.loads(datafile.read())

    for obj in reference_data['regions']:
        Region.objects.get_or_create(**obj)

    enchantment_levels = ['I', 'II', 'III', 'IV', 'V']
    for obj in reference_data['enchantments']:
        if obj['max_level'] == 1:
            Enchantment.objects.get_or_create(name=obj['name'])
        else:
            for i in range(obj['max_level']):
                Enchantment.objects.get_or_create(name=obj['name'] + " " + enchantment_levels[i])

    for obj in reference_data['potions']:
        Potion.objects.get_or_create(name=obj['name'])
        Potion.objects.get_or_create(name=obj['name'] + " (Splash)")
        Potion.objects.get_or_create(name=obj['name'] + " (Lingering)")

    for obj in reference_data['items']:
        potions = None
        if "potions" in obj:
            potions = Potion.objects.filter(name__in=obj["potions"])

        item, _ = Item.objects.get_or_create(name=obj['name'],
                                             is_enchantable=obj.get('is_enchantable', False),
                                             is_potion=obj.get('is_potion', False))

        if potions:
            [ItemIcon.objects.get_or_create(item=item,
                                            enchanted=obj.get("enchanted", False),
                                            potion=potion,
                                            icon=obj["icon"]
                                            ) for potion in potions]
        else:
            ItemIcon.objects.get_or_create(item=item,
                                            enchanted=obj.get("enchanted", False),
                                            potion=None,
                                            icon=obj["icon"]
                                            )

        for item_class in obj.get("classes", []):
            ItemClass.objects.get_or_create(item=item, name=item_class)

    for obj in reference_data['mobs']:
        Mob.objects.get_or_create(**obj)

    return redirect(reverse('index'))
