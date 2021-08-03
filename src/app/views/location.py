from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.models.locations import Maintainer, Location, StockRecord
from app.models.users import UserDetails


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
    pagination = 25
    page = int(request.GET.get("page", 0))
    results = page * pagination

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
    all_stock = all_stock[results:results + pagination]
    [s.set_display_data(request.user) for s in all_stock]

    context = {
        "all_stock": all_stock,
        "is_maintainer": request.user in [m.user for m in maintainers],
        "location": location,
        "maintainers": maintainer_details
    }
    if len(all_stock) == pagination:
        context["next_page"] = page + 1
    if page > 0:
        context['previous_page'] = page - 1

    return render(request, template_name, context)
