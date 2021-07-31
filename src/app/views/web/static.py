from django.shortcuts import render





def under_construction(request):
    template_name = 'under_construction.html'
    return render(request, template_name)
