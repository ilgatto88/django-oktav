from django.db import models

# Create your models here.
class Bundesland(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Municipality(models.Model):
    name = models.CharField(max_length=100)
    gkz = models.PositiveIntegerField()
    bundesland = models.CharField(max_length=100)

    def __str__(self):
        return self.name