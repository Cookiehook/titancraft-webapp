from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from app.models.constants import Enchantment, Potion, Item
from app.models.locations import Maintainer, Location
from app.models.stock import StockRecord
from app.models.users import UserDetails
from app.utils import is_maintainer


@login_required()
def modify_location(request, slug):
    template_name = 'pages/modify_location.html'
    if not is_maintainer(request.user, slug=slug):
        return redirect(reverse("not_authorised"))

    location = Location.objects.get(slug=slug)
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
    if not is_maintainer(request.user, slug=slug):
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
        stock_record.set_display_data(request.user)
        context['stock_record'] = stock_record

    return render(request, template_name, context)


@login_required()
def modify_services(request, slug):
    template_name = 'pages/modify_services.html'
    if not is_maintainer(request.user, slug=slug):
        return redirect(reverse("not_authorised"))

    context = {

    }
    return render(request, template_name, context)


@login_required()
def modify_farmables(request, slug):
    template_name = 'pages/modify_farmables.html'
    if not is_maintainer(request.user, slug=slug):
        return redirect(reverse("not_authorised"))

    context = {

    }
    return render(request, template_name, context)
