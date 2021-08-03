import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe

from app.models.constants import Enchantment, Potion, Item
from app.models.locations import Maintainer, Location, StockRecord, EnchantmentToStockRecord, PotionToStockRecord
from app.models.users import UserDetails


def is_maintainer(user, slug):
    location = Location.objects.get(slug=slug)
    maintainers = Maintainer.objects.filter(location=location)
    return user in [m.user for m in maintainers]


@login_required()
def modify_location(request, slug):
    template_name = 'pages/modify_location.html'
    if not is_maintainer(request.user, slug):
        return redirect(reverse("not_authorised"))

    location = Location.objects.get(slug=slug)
    context = {
        "location": location
    }
    return render(request, template_name, context)


@login_required()
def modify_maintainers(request, slug):
    template_name = 'pages/modify_maintainers.html'
    location = Location.objects.get(slug=slug)
    if not is_maintainer(request.user, slug):
        return redirect(reverse("not_authorised"))

    maintainers = Maintainer.objects.filter(location=location)
    for maintainer in maintainers:
        details = UserDetails.objects.get(user=maintainer.user)
        maintainer.avatar = f"https://cdn.discordapp.com/avatars/{details.discord_id}/{details.avatar_hash}.png"

    context = {
        "location": location,
        "maintainers": maintainers,
        "users": User.objects.all()
    }
    return render(request, template_name, context)


@login_required()
def modify_stock(request, slug):
    template_name = 'pages/modify_stock.html'
    if not is_maintainer(request.user, slug):
        return redirect(reverse("not_authorised"))

    enchantments = Enchantment.objects.all().order_by("name")
    potions = Potion.objects.all().order_by("name")

    context = {
        "items": Item.objects.all().order_by("name"),
        "location": Location.objects.get(slug=slug),
        "enchantments": enchantments,
        "potions": potions,
        "enchantment_height": int(len(enchantments) / 5)
    }
    if 'id' in request.GET:
        stock_record = StockRecord.objects.get(id=request.GET['id'])
        context['stock_record'] = stock_record
        context['current_enchantments'] = mark_safe([e.enchantment.name for e in EnchantmentToStockRecord.objects.filter(stock_record=stock_record)])
        context['current_potions'] = mark_safe([e.potion.name for e in PotionToStockRecord.objects.filter(stock_record=stock_record)])

    return render(request, template_name, context)


@login_required()
def modify_services(request, slug):
    template_name = 'pages/modify_services.html'
    if not is_maintainer(request.user, slug):
        return redirect(reverse("not_authorised"))

    context = {

    }
    return render(request, template_name, context)


@login_required()
def modify_farmables(request, slug):
    template_name = 'pages/modify_farmables.html'
    if not is_maintainer(request.user, slug):
        return redirect(reverse("not_authorised"))

    context = {

    }
    return render(request, template_name, context)


@login_required()
def update_availability(request):
    stock = StockRecord.objects.get(id=request.POST['id'])
    stock.units = int(request.POST['units'])
    stock.last_updated = datetime.datetime.utcnow()
    stock.save()
    return HttpResponse()


@login_required()
def add_stock(request):
    if "id" in request.POST:
        stock_record = StockRecord.objects.get(id=request.POST['id'])
    else:
        stock_record = StockRecord()
    stock_record.location = Location.objects.get(id=int(request.POST['location']))

    stock_record.stock_item = Item.objects.get(name=request.POST['stock_item'])
    stock_record.stock_description = request.POST['stock_description']
    stock_record.stock_stack_size = int(request.POST['stock_stack_size'])

    stock_record.cost_item = Item.objects.get(name=request.POST['cost_item'])
    stock_record.cost_stack_size = int(request.POST['cost_stack_size'])
    stock_record.units = int(request.POST['units'])
    stock_record.last_updated = datetime.datetime.utcnow()

    stock_record.save()

    # Clear old potions and enchantments
    EnchantmentToStockRecord.objects.filter(stock_record=stock_record).delete()
    PotionToStockRecord.objects.filter(stock_record=stock_record).delete()

    for enchantment_name in request.POST.getlist("enchantments"):
        enchantment = Enchantment.objects.get(name=enchantment_name)
        EnchantmentToStockRecord.objects.get_or_create(enchantment=enchantment, stock_record=stock_record)[0].save()

    for potion_name in request.POST.getlist("potions"):
        potion = Potion.objects.get(name=potion_name)
        PotionToStockRecord.objects.get_or_create(potion=potion, stock_record=stock_record)[0].save()

    return redirect(reverse('get_location', args=(stock_record.location.slug,)))
