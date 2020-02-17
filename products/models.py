from django.db import models

class ProductFeature(models.Model):
    name = models.CharField(max_length=100)
    print_name = models.CharField(max_length=100)
    function = models.CharField(max_length=100)
    dataset = models.CharField(max_length=100)
    selectable_rcp = models.BooleanField()
    output_types = models.CharField(max_length=100)
    widgets = models.CharField(max_length=100, default="")
    extra = models.CharField(max_length=200)

    def __str__(self):
        return self.print_name

class Widget(models.Model):
    name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=100)
    label = models.CharField(max_length=100, null=True, default="")
    enabled = models.BooleanField()

    def __str__(self):
        return self.name