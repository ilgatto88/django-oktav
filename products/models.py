from django.db import models

# Create your models here.
class ProductRequest(models.Model):
    product_type = models.CharField(max_length=40)
    parameter = models.CharField(max_length=30)
    parameter2 = models.CharField(max_length=30)
    aggregation_period = models.CharField(max_length=10)
    season = models.CharField(max_length=10)
    scenario = models.CharField(max_length=10)
    region_option = models.CharField(max_length=20)
    region = models.CommaSeparatedIntegerField()
    period_start = models.DateField()
    period_end = models.DateField()
    reference_period_start = models.DateField()
    reference_period_end = models.DateField()
    
