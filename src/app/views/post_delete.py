from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

from app.models.locations import Maintainer, Location
from app.models.stock import StockRecord, ServiceRecord, FarmRecord


@login_required()
def delete_maintainer(request):
    location = Location.objects.get(id=int(request.POST['location']))
    if not location.is_maintainer(request.user):
        return redirect(reverse("not_authorised"))

    maintainer = Maintainer.objects.get(id=request.POST['id'])
    location_id = maintainer.location.id
    maintainer.delete()
    return redirect(reverse("modify_location", args=(location_id,)))


@login_required()
def delete_location(request):
    location = Location.objects.get(id=int(request.POST['location']))
    if not location.is_maintainer(request.user):
        return redirect(reverse("not_authorised"))

    location.delete()
    return redirect(reverse("manage_locations"))


@login_required()
def delete_stock(request):
    stock_record = StockRecord.objects.get(id=request.POST['id'])
    if not stock_record.location.is_maintainer(request.user):
        return redirect(reverse("not_authorised"))

    location_id = stock_record.location.id
    stock_record.delete()
    return redirect(reverse("get_location", args=(location_id,)))


@login_required()
def delete_service(request):
    service_record = ServiceRecord.objects.get(id=request.POST['id'])
    if not service_record.location.is_maintainer(request.user):
        return redirect(reverse("not_authorised"))

    location_id = service_record.location.id
    service_record.delete()
    return redirect(reverse("get_location", args=(location_id,)))


@login_required()
def delete_farm(request):
    location = Location.objects.get(id=request.POST['location'])
    if not location.is_maintainer(request.user):
        return redirect(reverse("not_authorised"))

    FarmRecord.objects.filter(location=location).delete()

    return redirect(reverse("get_location", args=(location.id,)))
