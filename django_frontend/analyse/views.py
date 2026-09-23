from django.shortcuts import render


def analyse(request):
    return render(request, "analyse/analyse.html")
