from django.shortcuts import render
from django.http import HttpResponse
from .models import Municipality, Bundesland
import json

def fetch_regions(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        qtype = request.GET.get('type', '')
        if qtype == 'bundesland':
            selected_regions = Bundesland.objects.filter(name__istartswith = q)
        elif qtype == 'municipality':
            selected_regions = Municipality.objects.filter(name__istartswith = q)
        results = []
        for mn in selected_regions:
            mn_json = {'value': mn.name}
            results.append(mn_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
