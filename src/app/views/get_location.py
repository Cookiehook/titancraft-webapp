from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from app import utils
from app.models.constants import Region
from app.models.locations import Maintainer, Location
from app.models.stock import StockRecord, ServiceRecord
from app.models.users import UserDetails


@login_required()
def manage_locations(request):
    template_name = 'pages/manage_locations.html'
    locations = [m.location for m in Maintainer.objects.filter(user=request.user)]
    context = {
        "locations": locations,
        "regions": Region.objects.all()
    }
    return render(request, template_name, context)


@login_required()
def get_location(request, id):
    template_name = 'pages/get_location.html'

    location = Location.objects.get(id=id)
    location.set_display_data(request.user)
    maintainers = Maintainer.objects.filter(location=location)

    maintainer_details = []
    for maintainer in maintainers:
        details = UserDetails.objects.get(user=maintainer.user)
        maintainer_details.append({
            "username": maintainer.user.username,
            "avatar": f"https://cdn.discordapp.com/avatars/{details.discord_id}/{details.avatar_hash}.png"
        })

    all_stock = StockRecord.objects.filter(location=location).order_by("-last_updated")
    [s.set_display_data(request.user) for s in all_stock]

    all_services = ServiceRecord.objects.filter(location=location).order_by("name")
    [s.set_display_data(request.user) for s in all_services]

    context = {
        "all_stock": all_stock,
        "all_services": all_services,
        "location": location,
        "maintainers": maintainer_details
    }

    farm_records = utils.get_farms_for_locations(Location.objects.filter(id=id), request.user)
    if farm_records[location]:
        context["all_farms"] = farm_records

    return render(request, template_name, context)


@login_required()
def get_map(request, region_id):
    template_name = 'pages/get_map.html'

    region = Region.objects.get(name="Shopping District")
    locations = [{
        "name": l.name,
        "x_pos": l.x_pos,
        "z_pos": l.z_pos
    } for l in Location.objects.filter(region=region)]

    context = {
        "region": {"name": region.name, "x_pos": region.x_pos, "z_pos": region.z_pos},
        "locations": locations
    }
    return render(request, template_name, context)
