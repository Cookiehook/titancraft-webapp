from copy import copy
from functools import reduce
from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from app.models.constants import Region, Item, ItemClass, Enchantment, Potion
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
        search_term = request.GET['search']
        all_stock = []
        all_itemstacks = []

        # In order, search for items that:
        #   Name exactly matches the search term
        #   Name contains the search term (excluding already found)
        #   Name contains a word from the search term (excluding already found)
        #   Items in the same class as exact or close matches
        #   Class contains a word from the search term (excluding already found)
        any_word_query = reduce(lambda q, f: q | Q(name__icontains=f), search_term.split(), Q())
        match_exact_items = Item.objects.filter(name__iexact=search_term).all()
        match_close_items = Item.objects.filter(name__icontains=search_term).exclude(id__in=match_exact_items).all()
        match_single_word_items = Item.objects.filter(Q(any_word_query & ~Q(id__in=match_exact_items | match_close_items)))
        classes = ItemClass.objects.filter(item__in=match_exact_items | match_close_items)
        match_class_items = ItemClass.objects.filter(Q(Q(name__in=classes.values('name')) & ~Q(item__in=match_exact_items | match_close_items | match_single_word_items))).values("item")
        match_class_name_items = ItemClass.objects.filter(Q(any_word_query & ~Q(item__in=match_exact_items | match_close_items | match_single_word_items))).values("item")

        # Fetch ItemStackToStockRecords matching the items found above, in that order
        all_itemstacks.append(ItemStackToStockRecord.objects.filter(item__in=match_exact_items      ).filter(enchantment_filter).filter(potion_filter).values("stock_record"))
        all_itemstacks.append(ItemStackToStockRecord.objects.filter(item__in=match_close_items      ).filter(enchantment_filter).filter(potion_filter).values("stock_record"))
        all_itemstacks.append(ItemStackToStockRecord.objects.filter(item__in=match_single_word_items).filter(enchantment_filter).filter(potion_filter).values("stock_record"))
        all_itemstacks.append(ItemStackToStockRecord.objects.filter(item__in=match_class_items      ).filter(enchantment_filter).filter(potion_filter).values("stock_record"))
        all_itemstacks.append(ItemStackToStockRecord.objects.filter(item__in=match_class_name_items ).filter(enchantment_filter).filter(potion_filter).values("stock_record"))

        # Get the parent StockRecords
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

    # TODO - Search
    all_farms = FarmRecord.objects.all()

    all_farms = all_farms[results:results + utils.PAGINATION]
    context = {
        "all_farms": all_farms
    }
    utils.set_pagination_details(request.GET, all_farms, page, context)
    return render(request, template_name, context)


@login_required()
def list_locations(request, region):
    template_name = 'pages/list_locations.html'
    page = int(request.GET.get("page", 0))
    results = page * utils.PAGINATION

    if 'search' not in request.GET or 'all' in request.GET:
        all_locations = Location.objects.filter(region=Region.objects.get(name=region)).order_by("spawn_distance")[results:results + pagination]
    else:
        search_term = request.GET['search']
        all_locations = Location.objects.filter(
            Q(region=Region.objects.get(name=region)) & (Q(name__icontains=search_term) | Q(description__icontains=search_term))).order_by("spawn_distance")

    context = {
        "all_locations": all_locations,
        "search_placeholder": f"Search {region}...",
        "search_suggestions": [l.name for l in all_locations],
    }

    utils.set_pagination_details(request.GET, all_locations, page, context)
    return render(request, template_name, context)
