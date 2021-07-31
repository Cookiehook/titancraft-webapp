from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from app.models.businesses import StaffMember


@login_required()
def manage_locations(request):
    template = "manage_locations.html"
    businesses = [s.business for s in StaffMember.objects.filter(user=request.user)]

    context = {
        "businesses": businesses
    }

    return render(request, template, context)
