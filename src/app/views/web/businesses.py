import logging

from django.shortcuts import render

from app.models.businesses import StockRecord
from app.models.constants import Item, ItemClass, ItemIcon

logger = logging.getLogger()


def list_all_stock(request):
    template = "list_all_stock.html"
    page = int(request.GET.get("page", 0))
    results = page * 25

    all_stock = StockRecord.objects.all()[results:results + 25]
    items = {i.name for i in Item.objects.all()}
    items.update({c.name for c in ItemClass.objects.all()})

    for stock in all_stock:
        stock_enchanted = True if stock.enchantment_set.all() else False
        stock_potion = stock.potion_set.all()[0].potion_type if stock.potion_set.all() else None
        if stock_enchanted:
            stock.stock_labels = [str(i) for i in stock.enchantment_set.all()]
        elif stock_potion:
            stock.stock_labels = [str(i) for i in stock.potion_set.all()]
        try:
            stock.stock_icon = ItemIcon.objects.get(item=stock.stock_item, enchanted=stock_enchanted, potion=stock_potion).icon
        except Exception as e:
            logger.warning(f"Couldn't find icon for {stock.stock_item} Enchanted={stock_enchanted} Potion={stock_potion}")
            stock.stock_icon = ItemIcon.objects.filter(item=stock.stock_item)[0].icon

        try:
            stock.cost_icon = ItemIcon.objects.get(item=stock.cost_item, enchanted=False, potion=None).icon
        except Exception as e:
            logger.warning(
                f"Couldn't find icon for {stock.cost_item} Enchanted=None Potion=None")
            stock.stock_icon = ItemIcon.objects.filter(item=stock.stock_item)[0].icon

    context = {
        "stock": all_stock,
        "items": sorted(items),
        "include_business": True,
        "next_page": page + 1,
    }
    if page > 0:
        context['previous_page'] = page - 1
    return render(request, template, context)
