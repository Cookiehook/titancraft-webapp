from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

from app.models.locations import Maintainer, Location
from app.models.stock import StockRecord, ServiceRecord
from app.utils import is_maintainer


@login_required()
def delete_maintainer(request):
    if not is_maintainer(request.user, id=int(request.POST['location'])):
        return redirect(reverse("not_authorised"))

    maintainer = Maintainer.objects.get(id=request.POST['id'])
    location_slug = maintainer.location.slug
    maintainer.delete()
    return redirect(reverse("modify_location", args=(location_slug,)))


@login_required()
def delete_location(request):
    if not is_maintainer(request.user, id=int(request.POST['location'])):
        return redirect(reverse("not_authorised"))

    Location.objects.get(id=int(request.POST['location'])).delete()
    return redirect(reverse("manage_locations"))


@login_required()
def delete_stock(request):
    stock_record = StockRecord.objects.get(id=request.POST['id'])
    if not is_maintainer(request.user, id=stock_record.location.id):
        return redirect(reverse("not_authorised"))

    location_slug = stock_record.location.slug
    stock_record.delete()
    return redirect(reverse("get_location", args=(location_slug,)))


@login_required()
def delete_service(request):
    service_record = ServiceRecord.objects.get(id=request.POST['id'])
    if not is_maintainer(request.user, id=service_record.location.id):
        return redirect(reverse("not_authorised"))

    location_slug = service_record.location.slug
    service_record.delete()
    return redirect(reverse("get_location", args=(location_slug,)))
