from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from app.models.constants import Enchantment, Potion, Item, Mob, Region
from app.models.locations import Maintainer, Location, Path
from app.models.stock import StockRecord, ServiceRecord, FarmRecord
from app.models.users import UserDetails


@login_required()
def modify_location(request, id):
    template_name = 'pages/modify_location.html'
    location = Location.objects.get(id=id)
    if not location.is_maintainer(request.user):
        return redirect(reverse("not_authorised"))

    location.set_display_data(request.user)
    maintainers = Maintainer.objects.filter(location=location)
    for maintainer in maintainers:
        details = UserDetails.objects.get(user=maintainer.user)
        maintainer.avatar = f"https://cdn.discordapp.com/avatars/{details.discord_id}/{details.avatar_hash}.png"

    context = {
        "location": location,
        "maintainers": maintainers,
        "users": User.objects.all(),
        "regions": Region.objects.all()

    }
    return render(request, template_name, context)


@login_required()
def modify_stock(request, id):
    template_name = 'pages/modify_stock.html'
    location = Location.objects.get(id=id)
    if not location.is_maintainer(request.user):
        return redirect(reverse("not_authorised"))

    location.set_display_data(request.user)
    enchantments = Enchantment.objects.all().order_by("name")
    potions = Potion.objects.all().order_by("name")

    context = {
        "items": Item.objects.all().order_by("name"),
        "location": location,
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
def modify_service(request, id):
    template_name = 'pages/modify_service.html'
    location = Location.objects.get(id=id)
    if not location.is_maintainer(request.user):
        return redirect(reverse("not_authorised"))

    location.set_display_data(request.user)

    context = {
        'location': location
    }

    if 'id' in request.GET:
        context['service'] = ServiceRecord.objects.get(id=request.GET['id'])

    return render(request, template_name, context)


@login_required()
def modify_farm(request, id):
    template_name = 'pages/modify_farm.html'
    location = Location.objects.get(id=id)
    if not location.is_maintainer(request.user):
        return redirect(reverse("not_authorised"))

    location.set_display_data(request.user)
    current_records = FarmRecord.objects.filter(location=location)
    [f.set_display_data(request.user) for f in current_records]

    context = {
        "location": location,
        "items": Item.objects.all().order_by("name"),
        "mobs": Mob.objects.all().order_by("name"),
        "current_records": [f.view_data for f in current_records],
    }

    return render(request, template_name, context)


@login_required()
def modify_path(request, id=None):
    if not request.user.is_staff:
        return redirect(reverse("not_authorised"))

    template_name = 'pages/modify_path.html'
    context = {
        "regions": Region.objects.all()
    }
    if id:
        path = Path.objects.get(id=id)
        context['path'] = path.get_display_data()

    return render(request, template_name, context)
