from django.shortcuts import render
from django.http import HttpResponse
from .models import Municipality
import json

def fetch_regions(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        selected_municipalities = Municipality.objects.filter(name__startswith = q)
        results = []
        for mn in selected_municipalities:
            mn_json = {'value': mn.name}
            results.append(mn_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
