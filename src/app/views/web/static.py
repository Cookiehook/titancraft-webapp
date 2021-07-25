from django.shortcuts import render


def index(request):
    template_name = 'index.html'
    return render(request, template_name)


def under_construction(request):
    template_name = 'under_construction.html'
    return render(request, template_name)
