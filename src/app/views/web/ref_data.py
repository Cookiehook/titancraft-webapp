import datetime
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse

# from app.models.businesses import Business, StaffMember, StockRecord
# from app.models.constants import BusinessType, EnchantmentLevel, EnchantmentType, \
#     PotionModifier, PotionType, Item, ItemIcon, ItemClass, Mob, Dimension
# from app.models.users import UserDetails


@login_required()
def initialise(request):
    if not request.user.is_staff:
        return HttpResponseForbidden(b'Only staff may use this endpoint')

    with open("base_data.json") as datafile:
        base_data = json.loads(datafile.read())

    for obj in base_data['dimensions']:
        Dimension.objects.get_or_create(**obj)

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

        item, _ = Item.objects.get_or_create(name=obj['name'],
                                             is_enchantable=obj.get('is_enchantable', False),
                                             is_potion=obj.get('is_potion', False))

        ItemIcon.objects.get_or_create(item=item,
                                       enchanted=obj.get("enchanted", False),
                                       potion=potion,
                                       icon=obj["icon"]
                                       )
        for item_class in obj.get("classes", []):
            ItemClass.objects.get_or_create(item=item, name=item_class)

    for obj in base_data['mobs']:
        Mob.objects.get_or_create(**obj)

    return redirect(reverse('index'))


@login_required()
def create_test_businesses(request):
    if not request.user.is_staff:
        return HttpResponseForbidden(b'Only staff may use this endpoint')
    business, _ = Business.objects.get_or_create(name="Cookiehook's Debug shop",
                                                 type=BusinessType.objects.get(name="Shop"),
                                                 slug="cookiehooks-debug-shop",
                                                 description="A shop entry for debugging the webapp. Don't try to go here, it doesn't exist",
                                                 x_pos=0,
                                                 y_pos=0,
                                                 z_pos=0,
                                                 dimension=Dimension.objects.get(name="Overworld"))
    user, _ = User.objects.get_or_create(username="Cookiehook", is_staff=True)
    user.save()
    business.save()
    user_detail, created = UserDetails.objects.get_or_create(user=user)
    if created:
        user_detail.discord_id = "158265153782022144"
        user_detail.avatar_hash = "6708d3305c4d6e160173c71b7d089e96"
        user_detail.save()
    StaffMember.objects.get_or_create(business=business, user=user)[0].save()

    farm, _ = Business.objects.get_or_create(name="Cookiehook's Debug farm",
                                                 type=BusinessType.objects.get(name="Farm"),
                                                 slug="cookiehooks-debug-farm",
                                                 description="A farm entry for debugging the webapp. Don't try to go here, it doesn't exist",
                                                 x_pos=0,
                                                 y_pos=0,
                                                 z_pos=0,
                                                 dimension=Dimension.objects.get(name="Overworld"))
    StaffMember.objects.get_or_create(business=farm, user=user)[0].save()

    location, _ = Business.objects.get_or_create(name="Cookiehook's Debug Location",
                                                 type=BusinessType.objects.get(name="Location"),
                                                 slug="cookiehooks-debug-farm",
                                                 description="A location entry for debugging the webapp. Don't try to go here, it doesn't exist",
                                                 x_pos=0,
                                                 y_pos=0,
                                                 z_pos=0,
                                                 dimension=Dimension.objects.get(name="Overworld"))
    StaffMember.objects.get_or_create(business=location, user=user)[0].save()

    # Create shop stock records
    diamond = Item.objects.get(name="Diamond")
    ench_level = EnchantmentLevel.objects.get(name="III")
    pot_strong = PotionModifier.objects.get(name="Strong")
    pot_splash = PotionModifier.objects.get(name="Splash")
    for item in Item.objects.all():
        # Create 1 unenchanted / unpotioned instance, then stock the modifiers
        stock_base = StockRecord(business=business,
                                 stock_item=item, stock_description="debug", stock_stack_size=64,
                                 cost_item=diamond, cost_description="debug diamond", cost_stack_size=8,
                                 units=12,
                                 last_updated=datetime.datetime.now())
        stock_base.save()
        if item.is_enchantable:
            for ench_type in EnchantmentType.objects.all():
                stock_1 = StockRecord(business=business,
                                      stock_item=item, stock_description="debug", stock_stack_size=64,
                                      cost_item=diamond, cost_description="debug diamond", cost_stack_size=8,
                                      units=12,
                                      last_updated=datetime.datetime.now())
                stock_2 = StockRecord(business=business,
                                      stock_item=item, stock_description="debug", stock_stack_size=64,
                                      cost_item=diamond, cost_description="debug diamond", cost_stack_size=8,
                                      units=12,
                                      last_updated=datetime.datetime.now())
                stock_1.save()
                stock_2.save()
                Enchantment(stock_record=stock_1, enchantment_type=ench_type, enchantment_level=ench_level).save()
                Enchantment(stock_record=stock_2, enchantment_type=ench_type, enchantment_level=ench_level).save()
                Enchantment(stock_record=stock_2, enchantment_type=ench_type, enchantment_level=ench_level).save()
        elif item.is_potion:
            for pot_type in PotionType.objects.all():
                stock_1 = StockRecord(business=business,
                                      stock_item=item, stock_description="debug", stock_stack_size=64,
                                      cost_item=diamond, cost_description="debug diamond", cost_stack_size=8,
                                      units=12,
                                      last_updated=datetime.datetime.now())
                stock_2 = StockRecord(business=business,
                                      stock_item=item, stock_description="debug", stock_stack_size=64,
                                      cost_item=diamond, cost_description="debug diamond", cost_stack_size=8,
                                      units=12,
                                      last_updated=datetime.datetime.now())
                stock_1.save()
                stock_2.save()
                potion_1 = Potion(stock_record=stock_1, potion_type=pot_type)
                potion_1.save()
                Potion(stock_record=stock_2, potion_type=pot_type).save()
                Potion(stock_record=stock_2, potion_type=pot_type).save()
                PotionModifierToPotion(potion_modifier=pot_strong, potion=potion_1).save()
                PotionModifierToPotion(potion_modifier=pot_splash, potion=potion_1).save()
    return redirect(reverse('index'))
