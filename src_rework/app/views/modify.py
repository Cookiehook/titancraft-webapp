from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from app.models.locations import Maintainer, Location
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

    context = {

    }
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
    return HttpResponse()
