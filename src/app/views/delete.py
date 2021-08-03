from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

from app.models.locations import Maintainer


@login_required()
def delete_maintainer(request):
    maintainer = Maintainer.objects.get(id=request.POST['id'])
    location_slug = maintainer.location.slug
    maintainer.delete()
    return redirect(reverse("modify_maintainers", args=(location_slug,)))
