import operator
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
    if enchantment_names := request.GET.getlist("enchantment"):
        enchantments = Enchantment.objects.filter(name__in=enchantment_names).all()
        enchantment_filter = Q(id__in=[e.item_stack.id for e in EnchantmentToItemStack.objects.filter(enchantment__in=enchantments)])

    if potion_names := request.GET.getlist("potion"):
        potions = Potion.objects.filter(name__in=potion_names).all()
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
        all_services = []

        search_term = request.GET['search']
        split_term_filter = reduce(lambda x, y: x | y, [(Q(name__icontains=word) | Q(description__icontains=word)) for word in search_term.split()])
        full_term_matches = ServiceRecord.objects.filter(Q(name__icontains=search_term) | Q(description__icontains=search_term))

        all_services.extend(full_term_matches)
        all_services.extend(ServiceRecord.objects.filter(split_term_filter).exclude(id__in=full_term_matches))

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

    if ('search' not in request.GET or request.GET.get('search') == '' and 'mob' not in request.GET and 'xp' not in request.GET) or 'all' in request.GET:
        farm_locations = FarmRecord.objects.distinct("location").values("location")
        locations = Location.objects.filter(id__in=farm_locations)
    else:
        item_filter = Q()
        mob_filter = Q()
        xp_filter = Q()
        if search_term := request.GET.get("search"):
            items = []
            [items.extend(i) for i in utils.search_item(search_term)]
            item_filter = Q(item__in=items)
        if mobs := request.GET.getlist("mob"):
            mob_filter = Q(mob__in=Mob.objects.filter(name__in=mobs))
        if 'xp' in request.GET:
            xp_filter = Q(xp=True)

        locations = [f.location for f in FarmRecord.objects.filter(item_filter & mob_filter & xp_filter)]

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
def list_locations(request):
    template_name = 'pages/list_locations.html'
    page = int(request.GET.get("page", 0))
    results = page * utils.PAGINATION

    if ('search' not in request.GET or request.GET.get('search') == '' and 'region' not in request.GET) or 'all' in request.GET:
        all_locations = Location.objects.order_by("spawn_distance")[results:results + utils.PAGINATION]
    else:
        region_filter = Q()
        search_filter = Q()
        if 'search' in request.GET and request.GET.get('search') != '':
            search_term = request.GET['search']
            split_term_filter = reduce(lambda x, y: x | y, [(Q(name__icontains=word) | Q(description__icontains=word)) for word in search_term.split()])
            search_filter = Q(name__icontains=search_term) | Q(description__icontains=search_term) | Q(split_term_filter)

        if 'region' in request.GET:
            parent_regions = Region.objects.filter(name__in=request.GET.getlist('region'))
            region_filter = Q(region__in=Region.objects.filter(parent__in=parent_regions)) | Q(region__in=parent_regions)

        all_locations = Location.objects.filter(region_filter & search_filter).order_by("spawn_distance")

    if 'x_pos' in request.GET and 'z_pos' in request.GET and \
            request.GET.get('x_pos') != '' and request.GET.get('z_pos') != '':
        x_centre = int(request.GET.get('x_pos'))
        z_centre = int(request.GET.get('z_pos'))
        [l.set_player_distance(x_centre, z_centre) for l in all_locations]
        all_locations = sorted(all_locations, key=lambda l: l.player_distance)

    context = {
        "regions": Region.objects.all(),
        "all_locations": all_locations,
        "search_placeholder": f"Search for Location...",
        "location_suggestions": [l.name for l in all_locations],
        "x_pos": request.GET.get("x_pos"),
        "z_pos": request.GET.get("z_pos"),
        "region": request.GET.getlist('region', []),
        "search_term": request.GET.get("search", "")
    }

    utils.set_pagination_details(request.GET, all_locations, page, context)
    return render(request, template_name, context)


def how_to(request):
    template_name = "pages/how_to.html"
    return render(request, template_name)
