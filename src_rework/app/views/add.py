from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse

from app.models.constants import Region
from app.models.locations import Location, Maintainer


@login_required()
def add_location(request):
    location, _ = Location.objects.get_or_create(name=request.POST['name'])
    if request.POST.get("delete"):
        location.delete()
        return redirect(reverse("manage_locations"))

    location.description = request.POST['description']
    location.x_pos = int(request.POST['x_pos'])
    location.y_pos = int(request.POST['y_pos'])
    location.z_pos = int(request.POST['z_pos'])
    location.region = Region.objects.get(name=request.POST['region'])

    location.save()
    maintainer, _ = Maintainer.objects.get_or_create(
        location=location,
        user=request.user
    )
    maintainer.save()
    return redirect(reverse("get_location", args=(location.slug,)))


@login_required()
def add_maintainer(request):
    location = Location.objects.get(id=request.POST['location'])
    maintainer = Maintainer(
        location=location,
        user=User.objects.get(id=request.POST['user'])
    )
    maintainer.save()
    return redirect(reverse("modify_maintainers", args=(location.slug,)))

