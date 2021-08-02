from functools import reduce

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from app.models.constants import Region, Item, ItemClass, Enchantment, Potion
from app.models.locations import Location, StockRecord, EnchantmentToStockRecord, PotionToStockRecord


@login_required()
def list_stock(request):
    template_name = 'pages/list_stock.html'
    pagination = 25
    page = int(request.GET.get("page", 0))
    results = page * pagination

    enchantment_filter = StockRecord.objects.all()
    potion_filter = StockRecord.objects.all()
    if enchantment_name := request.GET.get("enchantment"):
        enchantments = Enchantment.objects.filter(name__icontains=enchantment_name).all()
        if enchantments:
            enchantment_filter = EnchantmentToStockRecord.objects.filter(enchantment__in=enchantments).values("stock_record")

    if potion_name := request.GET.get("potion"):
        potions = Potion.objects.filter(name__icontains=potion_name).all()
        if potions:
            potion_filter = PotionToStockRecord.objects.filter(potion__in=potions).values("stock_record")

    if 'class' in request.GET:
        items = [i.item.id for i in ItemClass.objects.filter(name=request.GET['class'])]
        all_stock = StockRecord.objects.filter(stock_item__in=items).order_by("-last_updated")
    elif 'search' not in request.GET or request.GET.get('search') == '' or 'all' in request.GET:
        all_stock = StockRecord.objects.filter(id__in=enchantment_filter).filter(id__in=potion_filter).order_by("-last_updated")
    else:
        search_term = request.GET['search']
        all_stock = []

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
        match_class_items = ItemClass.objects.filter(name__in=classes.values('name')).values("item")
        match_class_name_items = ItemClass.objects.filter(Q(any_word_query & ~Q(item__in=match_exact_items | match_close_items | match_single_word_items))).values("item")

        # Fetch StockRecords matching the items found above, in that order
        all_stock.extend(StockRecord.objects.filter(stock_item__in=match_exact_items).filter(id__in=enchantment_filter).filter(id__in=potion_filter).order_by('-last_updated'))
        all_stock.extend(StockRecord.objects.filter(stock_item__in=match_close_items).filter(id__in=enchantment_filter).filter(id__in=potion_filter).order_by('-last_updated'))
        all_stock.extend(StockRecord.objects.filter(stock_item__in=match_single_word_items).filter(id__in=enchantment_filter).filter(id__in=potion_filter).order_by('-last_updated'))
        all_stock.extend(StockRecord.objects.filter(stock_item__in=match_class_items).filter(id__in=enchantment_filter).filter(id__in=potion_filter).order_by('-last_updated'))
        all_stock.extend(StockRecord.objects.filter(stock_item__in=match_class_name_items).filter(id__in=enchantment_filter).filter(id__in=potion_filter).order_by('-last_updated'))

    all_stock = all_stock[results:results + pagination]
    items = {i.name for i in Item.objects.all()}
    items.update({c.name for c in ItemClass.objects.all()})
    [s.set_display_data() for s in all_stock]

    context = {
        "all_stock": all_stock,
        "item_suggestions": Item.objects.all(),
        "enchantment_suggestions": Enchantment.objects.all(),
        "potion_suggestions": Potion.objects.all(),
        "all_classes": sorted({c.name for c in ItemClass.objects.all()})
    }

    if len(all_stock) == pagination:
        context["next_page"] = page + 1
    if page > 0:
        context['previous_page'] = page - 1
    if 'search' in request.GET and 'all' not in request.GET:
        context['search_term'] = request.GET['search']

    return render(request, template_name, context)


@login_required()
def list_services(request):
    template_name = 'pages/list_services.html'
    context = {}
    return render(request, template_name, context)


@login_required()
def list_farms(request):
    template_name = 'pages/list_farms.html'
    context = {}
    return render(request, template_name, context)


@login_required()
def list_locations(request, region):
    template_name = 'pages/list_locations.html'
    pagination = 25
    page = int(request.GET.get("page", 0))
    results = page * pagination

    if 'search' not in request.GET or 'all' in request.GET:
        locations = Location.objects.filter(region=Region.objects.get(name=region)).order_by("spawn_distance")[results:results + pagination]
    else:
        search_term = request.GET['search']
        locations = Location.objects.filter(
            Q(region=Region.objects.get(name=region)) & (Q(name__icontains=search_term) | Q(description__icontains=search_term))).order_by("spawn_distance")

    context = {
        "search_placeholder": f"Search {region}...",
        "locations": locations,
        "search_suggestions": [l.name for l in locations]
    }

    if len(locations) == pagination:
        context["next_page"] = page + 1
    if page > 0:
        context['previous_page'] = page - 1
    if 'search' in request.GET and 'all' not in request.GET:
        context['search_term'] = request.GET['search']

    return render(request, template_name, context)
