import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from app.models.constants import Region, Item, Enchantment, Potion, Mob
from app.models.locations import Location, Maintainer, Path, PathLink
from app.models.stock import StockRecord, PotionToItemStack, EnchantmentToItemStack, ItemStackToStockRecord, \
    ServiceRecord, FarmRecord


@login_required()
def upsert_location(request):
    if 'location' in request.POST:
        location = Location.objects.get(id=int(request.POST['location']))
        if not location.is_maintainer(request.user):
            return redirect(reverse("not_authorised"))
    else:
        location = Location(name=request.POST['name'])

    location.name = request.POST['name']
    location.description = request.POST['description']
    location.x_pos = int(request.POST['x_pos'])
    location.y_pos = int(request.POST['y_pos'])
    location.z_pos = int(request.POST['z_pos'])
    location.region = Region.objects.get(name=request.POST['region'])

    location.save()
    maintainer, _ = Maintainer.objects.get_or_create(
        location=location,
        user=request.user
    )
    maintainer.save()
    return redirect(reverse("get_location", args=(location.id,)))


@login_required()
def upsert_maintainer(request):
    location = Location.objects.get(id=request.POST['location'])
    if not location.is_maintainer(request.user):
        return redirect(reverse("not_authorised"))

    maintainer, _ = Maintainer.objects.get_or_create(
        location=location,
        user=User.objects.get(id=request.POST['user'])
    )
    maintainer.save()
    return redirect(reverse("modify_location", args=(location.id,)))


@login_required()
def upsert_stock(request):
    location = Location.objects.get(id=int(request.POST['location']))
    if not location.is_maintainer(request.user):
        return redirect(reverse("not_authorised"))

    if "id" in request.POST:
        stock_record = StockRecord.objects.get(id=request.POST['id'])
    else:
        stock_record = StockRecord()

    stock_record.location = Location.objects.get(id=int(request.POST['location']))
    stock_record.cost_item = Item.objects.get(name=request.POST['cost_item'])
    stock_record.cost_stack_size = int(request.POST['cost_stack_size'])
    stock_record.units = int(request.POST['units'])
    stock_record.last_updated = datetime.datetime.utcnow()
    stock_record.save()

    num_stacks = len([key for key in request.POST if key.startswith("stock_item_")])

    # Delete and re-create all itemstacks for this record. Otherwise, orphans would accumulate
    # when users change the item for sale. Enchantments and Potions are implicitly deleted by DB relationship.
    ItemStackToStockRecord.objects.filter(stock_record=stock_record).delete()
    for i in range(1, num_stacks + 1):
        if request.POST[f"stock_item_{i}"] == "":
            continue  # Likely a hanging empty itemstack fieldset. Ignore it

        item = Item.objects.get(name=request.POST[f"stock_item_{i}"])
        stack_size = (int(request.POST[f"stock_stacks_{i}"]) * 64) + (int(request.POST[f"stock_items_{i}"]))
        description = request.POST[f"stock_description_{i}"]
        enchantments = request.POST.getlist(f"enchantments_{i}", [])
        potions = request.POST.getlist(f"potions_{i}", [])

        item_stack = ItemStackToStockRecord(stock_record=stock_record, item=item,
                                            description=description, stack_size=stack_size)
        item_stack.save()

        for enchantment_name in enchantments:
            enchantment = Enchantment.objects.get(name=enchantment_name)
            EnchantmentToItemStack(enchantment=enchantment, item_stack=item_stack).save()
        for potion_name in potions:
            potion = Potion.objects.get(name=potion_name)
            PotionToItemStack(potion=potion, item_stack=item_stack).save()

    if 'add-another' in request.POST:
        return redirect(reverse('modify_stock', args=(stock_record.location.id,)))
    else:
        return redirect(reverse('get_location', args=(stock_record.location.id,)))


@login_required()
def update_availability(request):
    """Called Async from form in page, and returns empty response"""
    stock = StockRecord.objects.get(id=request.POST['id'])
    stock.units = int(request.POST['units'])
    stock.last_updated = datetime.datetime.utcnow()
    stock.save()
    return HttpResponse()


@login_required()
def upsert_service(request):
    location = Location.objects.get(id=int(request.POST['location']))
    if not location.is_maintainer(request.user):
        return redirect(reverse("not_authorised"))

    if "service" in request.POST:
        service_record = ServiceRecord.objects.get(id=request.POST["service"])
    else:
        service_record = ServiceRecord(
            location=Location.objects.get(id=int(request.POST['location'])),
        )
    service_record.name = request.POST['name']
    service_record.description = request.POST['description']
    service_record.save()

    return redirect(reverse('get_location', args=(service_record.location.id,)))


@login_required()
def upsert_farm(request):
    location = Location.objects.get(id=int(request.POST['location']))
    if not location.is_maintainer(request.user):
        return redirect(reverse("not_authorised"))
    FarmRecord.objects.filter(location=location).delete()

    for key, value in request.POST.items():
        if value == "":
            continue  # Empty values left by unused fieldsets
        if key.startswith("item"):
            FarmRecord(location=location,item=Item.objects.get(name=value)).save()
        if key.startswith("mob"):
            mob_num = key[-1]
            FarmRecord(
                location=location,
                mob=Mob.objects.get(name=value),
                xp=f"xp_{mob_num}" in request.POST  # Checkboxes only appear if they are selected
            ).save()

    return redirect(reverse('get_location', args=(location.id,)))


@login_required()
def upsert_path(request):
    if not request.user.is_staff:
        return redirect(reverse("not_authorised"))

    region = Region.objects.get(name=request.POST['region'])
    if "path" in request.POST:
        path = Path.objects.get(id=request.POST['path'])
    else:
        path = Path(name=request.POST["name"])

    path.region = region
    path.save()

    PathLink.objects.filter(path=path).delete()
    num_points = len([key for key in request.POST if key.startswith("x_pos")])
    for i in range(1, num_points):
        if request.POST[f"x_pos_{i}"] == "":
            continue  # Likely a hanging empty fieldset. Ignore it

        PathLink(path=path,
                 position=i,
                 start_x=request.POST[f"x_pos_{i}"],
                 start_z=request.POST[f"z_pos_{i}"],
                 end_x=request.POST[f"x_pos_{i+1}"],
                 end_z=request.POST[f"z_pos_{i+1}"]).save()

    return redirect(reverse('manage_paths'))

