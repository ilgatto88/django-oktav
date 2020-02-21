"""weboktav URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from products import views as products_view
from region import views as region_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', products_view.index, name = 'index'),
    url(r'^products', products_view.product_request, name = 'products'),
    url(r'^result', products_view.product_result, name = 'product_result'),
    url(r'^api/get_regions/', region_views.fetch_regions, name = 'get_regions'),
    url(r'^api/get_product_features/', products_view.fetch_product_features, name = 'get_product_features'),
    url(r'^docs/', products_view.documentation, name = 'documentation')
]
