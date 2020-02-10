from django.shortcuts import render
from django.shortcuts import render
from .models import ProductRequest

# Create your views here.
def home(request):
    products_requests = ProductRequest.objects.all()
    return render(request, 'home.html', {'product_requests': products_requests})
