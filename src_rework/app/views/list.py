from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from app.models.constants import Region
from app.models.locations import Location


@login_required()
def list_stock(request):
    template_name = 'pages/list_stock.html'
    context = {}
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
        locations = Location.objects.filter(region=Region.objects.get(name=region))[results:results + pagination]
    else:
        search_term = request.GET['search']
        locations = Location.objects.filter(
            Q(region=Region.objects.get(name=region)) & (Q(name__icontains=search_term) | Q(description__icontains=search_term)))

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
