import datetime
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse

from app.models.constants import Region, Enchantment, Potion, Item, ItemIcon, ItemClass, Mob
from app.models.locations import Location, Maintainer, StockRecord, EnchantmentToStockRecord, PotionToStockRecord
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


@login_required()
def create_debug(request):
    if not request.user.is_staff:
        return HttpResponseForbidden(b'Only staff may use this endpoint')

    # Create single user
    user, _ = User.objects.get_or_create(username="Cookiehook")
    user.is_staff = True
    user.save()
    user_detail, created = UserDetails.objects.get_or_create(user=user)
    if created:
        user_detail.discord_id = "158265153782022144"
        user_detail.avatar_hash = "6708d3305c4d6e160173c71b7d089e96"
        user_detail.save()

    for region in Region.objects.all():
        for i in range(50):
            location, _ = Location.objects.get_or_create(
                name=f"Debug {region.name} Location #{i}",
                description=f"Debug {region.name} description #{i}",
                x_pos=i,
                y_pos=i,
                z_pos=i,
                region=region
            )
            location.save()
            Maintainer.objects.get_or_create(
                location=location,
                user=user
            )[0].save()

    # Create shop stock records
    shop = Location.objects.get(name="Debug Shopping-District Location #0")
    diamond = Item.objects.get(name="Diamond")
    for item in Item.objects.all():
        # Create 1 unenchanted / unpotioned instance, then stock the modifiers
        stock_base = StockRecord(location=shop,
                                 stock_item=item, stock_description="debug", stock_stack_size=64,
                                 cost_item=diamond, cost_stack_size=8,
                                 units=12,
                                 last_updated=datetime.datetime.utcnow())
        stock_base.save()
        if item.is_enchantable:
            for ench in Enchantment.objects.all():
                stock_1 = StockRecord(location=shop,
                                      stock_item=item, stock_description="debug", stock_stack_size=64,
                                      cost_item=diamond, cost_stack_size=8,
                                      units=12,
                                      last_updated=datetime.datetime.utcnow())
                stock_2 = StockRecord(location=shop,
                                      stock_item=item, stock_description="debug", stock_stack_size=64,
                                      cost_item=diamond, cost_stack_size=8,
                                      units=12,
                                      last_updated=datetime.datetime.utcnow())
                stock_1.save()
                stock_2.save()
                EnchantmentToStockRecord(enchantment=ench, stock_record=stock_1).save()
                EnchantmentToStockRecord(enchantment=ench, stock_record=stock_2).save()
                EnchantmentToStockRecord(enchantment=ench, stock_record=stock_2).save()
        elif item.is_potion:
            for potion in Potion.objects.all():
                stock_1 = StockRecord(location=shop,
                                      stock_item=item, stock_description="debug", stock_stack_size=64,
                                      cost_item=diamond, cost_stack_size=8,
                                      units=12,
                                      last_updated=datetime.datetime.utcnow())
                StockRecord(location=shop,
                            stock_item=item, stock_description="debug", stock_stack_size=64,
                            cost_item=diamond, cost_stack_size=8,
                            units=12,
                            last_updated=datetime.datetime.utcnow()).save()
                stock_1.save()
                PotionToStockRecord(potion=potion, stock_record=stock_1).save()

    return redirect(reverse('index'))
