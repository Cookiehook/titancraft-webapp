from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app import utils
from app.models.locations import Maintainer, Location
from app.models.stock import StockRecord, ServiceRecord
from app.models.users import UserDetails
from app.utils import is_maintainer


@login_required()
def manage_locations(request):
    template_name = 'pages/manage_locations.html'
    locations = [m.location for m in Maintainer.objects.filter(user=request.user)]
    context = {
        "locations": locations
    }
    return render(request, template_name, context)


@login_required()
def get_location(request, slug):
    template_name = 'pages/get_location.html'

    location = Location.objects.get(slug=slug)
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
        "is_maintainer": is_maintainer(request.user, slug=slug),
        "location": location,
        "maintainers": maintainer_details
    }

    return render(request, template_name, context)
