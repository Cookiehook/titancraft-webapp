import logging
from functools import reduce

from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse

from app.models.businesses import StockRecord, ServiceRecord, Business, StaffMember, FarmRecord
from app.models.constants import Item, ItemClass, ItemIcon, BusinessType
from app.models.users import UserDetails

logger = logging.getLogger()


def append_stock_icons(stock_list):
    for stock in stock_list:
        stock_enchanted = True if stock.enchantment_set.all() else False
        stock_potion = stock.potion_set.all()[0].potion_type if stock.potion_set.all() else None
        if stock_enchanted:
            stock.stock_labels = [str(i) for i in stock.enchantment_set.all()]
        elif stock_potion:
            stock.stock_labels = [str(i) for i in stock.potion_set.all()]
        try:
            stock.stock_icon = ItemIcon.objects.get(item=stock.stock_item, enchanted=stock_enchanted,
                                                    potion=stock_potion).icon
        except Exception as e:
            logger.warning(
                f"Couldn't find icon for {stock.stock_item} Enchanted={stock_enchanted} Potion={stock_potion}")
            stock.stock_icon = ItemIcon.objects.filter(item=stock.stock_item)[0].icon

        try:
            stock.cost_icon = ItemIcon.objects.get(item=stock.cost_item, enchanted=False, potion=None).icon
        except Exception as e:
            logger.warning(
                f"Couldn't find icon for {stock.cost_item} Enchanted=None Potion=None")
            stock.stock_icon = ItemIcon.objects.filter(item=stock.stock_item)[0].icon


def list_all_stock(request):
    template = "list_all_stock.html"
    pagination = 25
    page = int(request.GET.get("page", 0))
    results = page * pagination

    if 'search' not in request.GET or 'all' in request.GET:
        all_stock = StockRecord.objects.order_by("-last_updated").all()[results:results + pagination]
    else:
        all_stock = []
        search_term = request.GET['search']

        # In order, search for items that:
        #   Name exactly matches the search term
        #   Name contains the search term (excluding already found)
        #   Name contains a word from the search term (excluding already found)
        #   Class contains a word from the search term (excluding already found)
        any_word_query = reduce(lambda q, f: q | Q(name__icontains=f), search_term.split(), Q())
        match_exact_items = [i.id for i in Item.objects.filter(name=search_term)]
        match_close_items = [i.id for i in Item.objects.filter(name__icontains=search_term).exclude(id__in=match_exact_items)]
        match_single_word_items = [i.id for i in Item.objects.filter(Q(any_word_query & ~Q(id__in=match_exact_items + match_close_items)))]
        match_class_items = [i.item.id for i in ItemClass.objects.filter(Q(any_word_query & ~Q(item__in=match_exact_items + match_close_items + match_single_word_items)))]

        # Fetch StockRecords matching the items found above, in that order
        all_stock.extend(StockRecord.objects.filter(stock_item__in=match_exact_items).order_by('-last_updated'))
        all_stock.extend(StockRecord.objects.filter(stock_item__in=match_close_items).order_by('-last_updated'))
        all_stock.extend(StockRecord.objects.filter(stock_item__in=match_single_word_items).order_by('-last_updated'))
        all_stock.extend(StockRecord.objects.filter(stock_item__in=match_class_items).order_by('-last_updated'))
        all_stock = all_stock[results:results + 25]

    items = {i.name for i in Item.objects.all()}
    items.update({c.name for c in ItemClass.objects.all()})
    append_stock_icons(all_stock)

    context = {
        "stock": all_stock,
        "items": sorted(items),
        "include_business": True,
        "search_placeholder": 'I want to buy...',
        "buisness_type": "Shop",
        "form_action": reverse("get_all_stock")
    }
    if len(all_stock) == pagination:
        context["next_page"] = page + 1
    if page > 0:
        context['previous_page'] = page - 1
    if 'search' in request.GET and 'all' not in request.GET:
        context['search_term'] = request.GET['search']

    return render(request, template, context)


def list_all_services(request):
    template = "list_all_services.html"
    pagination = 25
    page = int(request.GET.get("page", 0))
    results = page * pagination

    if 'search' not in request.GET or 'all' in request.GET:
        all_services = ServiceRecord.objects.all()[results:results + pagination]
    else:
        search_term = request.GET['search']
        all_services = ServiceRecord.objects.filter(Q(name__icontains=search_term) | Q(description__icontains=search_term))

    context = {
        "services": all_services,
        "include_business": True,
        "search_placeholder": 'I need someone to...',
        "business_type": "Shop",
        "form_action": reverse("get_all_services")
    }

    if len(all_services) == pagination:
        context["next_page"] = page + 1
    if page > 0:
        context['previous_page'] = page - 1
    if 'search' in request.GET and 'all' not in request.GET:
        context['search_term'] = request.GET['search']

    return render(request, template, context)


def list_all_businesses(request, business_type):
    template = "list_all_businesses.html"
    pagination = 25
    page = int(request.GET.get("page", 0))
    results = page * pagination
    business_type_obj = BusinessType.objects.get(name=business_type)

    if 'search' not in request.GET or 'all' in request.GET:
        all_businesses = Business.objects.filter(type=business_type_obj)[results:results + pagination]
    else:
        search_term = request.GET['search']
        all_businesses = Business.objects.filter(Q(type=business_type_obj) & (Q(name__icontains=search_term) | Q(description__icontains=search_term)))

    context = {
        "businesses": all_businesses,
        "include_business": True,
        "search_placeholder": "I'm looking for...",
        "business_type": business_type,
        "form_action": reverse("get_all_businesses", args=(business_type,))
    }

    if len(all_businesses) == pagination:
        context["next_page"] = page + 1
    if page > 0:
        context['previous_page'] = page - 1
    if 'search' in request.GET and 'all' not in request.GET:
        context['search_term'] = request.GET['search']

    return render(request, template, context)


def get_single_business(request, slug):
    template = "get_single_business.html"
    business = Business.objects.get(slug=slug)

    staff_list = []
    for staff in StaffMember.objects.filter(business=business):
        details = UserDetails.objects.get(user=staff.user)
        staff_list.append({
            "username": staff.user.username,
            "avatar": f"https://cdn.discordapp.com/avatars/{details.discord_id}/{details.avatar_hash}.png"
        })

    all_stock = StockRecord.objects.filter(business=business).all()
    append_stock_icons(all_stock)

    context = {
        "business": business,
        "staff_list": staff_list,
        "stock": all_stock,
        "services": ServiceRecord.objects.filter(business=business),
        "farms": FarmRecord.objects.filter(business=business)
    }

    return render(request, template, context)
