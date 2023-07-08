from django.shortcuts import render
from django.urls import reverse

from .models import Channel


def search(request, keyword):
    results = Channel.objects.filter(url__icontains=keyword)
    print(results.count())
    data = dict(results=results, keyword=keyword)
    return render(request, "channel/search.html", data)


def import_file(request):
    data = request.FILES
    print(data)
    return render(request, "channel/import_file.html")
