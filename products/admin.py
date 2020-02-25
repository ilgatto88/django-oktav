from django.contrib import admin
from .models import ProductFeature, Widget, Parameter, AggregationPeriod, Season, Scenario
from .models import RegionOption, OutputType

admin.site.register(ProductFeature)
admin.site.register(Widget)
admin.site.register(Parameter)
admin.site.register(AggregationPeriod)
admin.site.register(Season)
admin.site.register(Scenario)
admin.site.register(RegionOption)
admin.site.register(OutputType)
