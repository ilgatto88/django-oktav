from django.db import models

class ProductFeature(models.Model):
    name = models.CharField(max_length=100)
    print_name = models.CharField(max_length=100)
    dataset = models.CharField(max_length=100)
    widgets = models.CharField(max_length=100)

    def __str__(self):
        return self.name