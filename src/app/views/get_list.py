from functools import reduce

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from app.models.constants import Region, Item, ItemClass, Enchantment, Potion, Mob
from app.models.locations import Location
from app.models.stock import StockRecord, EnchantmentToItemStack, PotionToItemStack, ItemStackToStockRecord, \
    ServiceRecord, FarmRecord
from app import utils


@login_required()
def list_stock(request):
    template_name = 'pages/list_stock.html'
    page = int(request.GET.get("page", 0))
    results = page * utils.PAGINATION

    enchantment_filter = Q()
    potion_filter =Q()
    if enchantment_name := request.GET.get("enchantment"):
        enchantments = Enchantment.objects.filter(name__icontains=enchantment_name).all()
        if enchantments:
            enchantment_filter = Q(id__in=[e.item_stack.id for e in EnchantmentToItemStack.objects.filter(enchantment__in=enchantments)])

    if potion_name := request.GET.get("potion"):
        potions = Potion.objects.filter(name__icontains=potion_name).all()
        if potions:
            potion_filter = Q(id__in=[p.item_stack.id for p in PotionToItemStack.objects.filter(potion__in=potions)])

    if 'class' in request.GET:
        items = [i.item.id for i in ItemClass.objects.filter(name=request.GET['class'])]
        all_stacks = ItemStackToStockRecord.objects.filter(item__in=items)
        all_stock = StockRecord.objects.filter(id__in=all_stacks.values("stock_record")).order_by("-last_updated")
    elif 'search' not in request.GET or request.GET.get('search') == '' or 'all' in request.GET:
        all_stacks = ItemStackToStockRecord.objects.filter(enchantment_filter).filter(potion_filter)
        all_stock = StockRecord.objects.filter(id__in=all_stacks.values("stock_record")).order_by("-last_updated")
    else:
        # Get all ItemStacks for relevant items
        all_itemstacks = []
        for item_group in utils.search_item(request.GET['search']):
            all_itemstacks.append(
                ItemStackToStockRecord.objects.filter(item__in=item_group).filter(enchantment_filter).filter(potion_filter).values("stock_record")
            )

        # Get the parent StockRecords for the itemstacks
        all_stock = []
        for stack_group in all_itemstacks:
            all_stock.extend(StockRecord.objects.filter(id__in=stack_group).order_by("-last_updated"))

    all_stock = all_stock[results:results + utils.PAGINATION]
    items = {i.name for i in Item.objects.all()}
    items.update({c.name for c in ItemClass.objects.all()})
    [s.set_display_data(request.user) for s in all_stock]

    context = {
        "all_stock": all_stock,
        "item_suggestions": Item.objects.all(),
        "enchantment_suggestions": Enchantment.objects.all(),
        "potion_suggestions": Potion.objects.all(),
        "all_classes": sorted({c.name for c in ItemClass.objects.all()}),
    }

    utils.set_pagination_details(request.GET, all_stock, page, context)
    return render(request, template_name, context)


@login_required()
def list_services(request):
    template_name = 'pages/list_services.html'
    page = int(request.GET.get("page", 0))
    results = page * utils.PAGINATION

    if 'search' not in request.GET or request.GET.get('search') == '' or 'all' in request.GET:
        all_services = ServiceRecord.objects.all()
    else:
        search_term = request.GET['search']
        all_services = ServiceRecord.objects.filter(Q(name__icontains=search_term) | Q(description__icontains=search_term))

    all_services = all_services[results:results + utils.PAGINATION]
    [s.set_display_data(request.user) for s in all_services]
    context = {
        "all_services": all_services,
        "search_placeholder": "Find a Service...",
    }

    utils.set_pagination_details(request.GET, all_services, page, context)
    return render(request, template_name, context)


@login_required()
def list_farms(request):
    template_name = 'pages/list_farms.html'
    page = int(request.GET.get("page", 0))
    results = page * utils.PAGINATION

    if ('search' not in request.GET or request.GET.get('search') == '' and 'mob' not in request.GET) or 'all' in request.GET:
        farm_locations = FarmRecord.objects.distinct("location").values("location")
        locations = Location.objects.filter(id__in=farm_locations)
    else:
        item_filter = Q()
        mob_filter = Q()
        if search_term := request.GET.get("search"):
            items = []
            [items.extend(i) for i in utils.search_item(search_term)]
            item_filter = Q(item__in=items)
        if mobs := request.GET.getlist("mob"):
            mob_filter = Q(mob__in=Mob.objects.filter(name__in=mobs))

        locations = [f.location for f in FarmRecord.objects.filter(item_filter | mob_filter)]

    locations = locations[results:results + utils.PAGINATION]
    all_farms = utils.get_farms_for_locations(locations, request.user)
    context = {
        "all_farms": all_farms,
        "item_suggestions": Item.objects.all(),
        "mobs": Mob.objects.all()
    }
    utils.set_pagination_details(request.GET, locations, page, context)
    return render(request, template_name, context)


@login_required()
def list_locations(request, region):
    template_name = 'pages/list_locations.html'
    page = int(request.GET.get("page", 0))
    results = page * utils.PAGINATION
    parent_region = Region.objects.get(name=region)
    region_filter = Q(region__in=Region.objects.filter(parent=parent_region)) | Q(region=parent_region)

    if 'search' not in request.GET or 'all' in request.GET:
        all_locations = Location.objects.filter(region_filter).order_by("spawn_distance")[results:results + utils.PAGINATION]
    else:
        search_term = request.GET['search']
        all_locations = Location.objects.filter(
            region_filter & (Q(name__icontains=search_term) | Q(description__icontains=search_term))).order_by("spawn_distance")

    context = {
        "all_locations": all_locations,
        "search_placeholder": f"Search {region}...",
        "search_suggestions": [l.name for l in all_locations],
    }

    utils.set_pagination_details(request.GET, all_locations, page, context)
    return render(request, template_name, context)


@login_required()
def how_to(request):
    template_name = "pages/how_to.html"
    return render(request, template_name)
