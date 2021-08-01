from django.contrib.auth.decorators import login_required
from django.shortcuts import render


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
    context = {}
    return render(request, template_name, context)
