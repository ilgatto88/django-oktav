import os
from django.db import models
from django.dispatch import receiver
from .storage import OverWriteStorage

class ProductFeature(models.Model):
    name = models.CharField(max_length=100)
    print_name = models.CharField(max_length=100)
    function = models.CharField(max_length=100)
    dataset = models.CharField(max_length=100)
    selectable_rcp = models.BooleanField()
    has_second_parameter = models.BooleanField(default = False)
    must_have_reference_period = models.BooleanField(default = False)
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

class Parameter(models.Model):
    name = models.CharField(max_length=100)
    print_name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    long_unit_name = models.CharField(max_length=100)
    rounding_digits = models.IntegerField()
    dtyope_out = models.CharField(max_length=10)
    scale_factor = models.FloatField()
    _FillValue = models.FloatField()

    def __str__(self):
        return self.print_name

class AggregationPeriod(models.Model):
    name = models.CharField(max_length=10)
    print_name = models.CharField(max_length=100)
    enabled_parameters = models.CharField(max_length=256, default='')

    def __str__(self):
        return self.print_name

class Season(models.Model):
    name = models.CharField(max_length=10)
    print_name = models.CharField(max_length=100)
    datum_start = models.CharField(max_length=10)
    datum_end = models.CharField(max_length=10)

    def __str__(self):
        return self.print_name

class Scenario(models.Model):
    name = models.CharField(max_length=10)
    print_name = models.CharField(max_length=100)

    def __str__(self):
        return self.print_name

class RegionOption(models.Model):
    name = models.CharField(max_length=20)
    print_name = models.CharField(max_length=100)

    def __str__(self):
        return self.print_name

class OutputType(models.Model):
    name = models.CharField(max_length=10)
    print_name = models.CharField(max_length=100)
    otype = models.CharField(max_length=100, default='None')

    def __str__(self):
        return self.name

class Analysis(models.Model):
    filename = models.CharField(max_length=256, null=False, default='')
    creation = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=256, null=False)
    analysis_details = models.TextField(default='')
    file = models.FileField(max_length=200, storage=OverWriteStorage())
    settings_json = models.TextField(default='', max_length=4096)

    @classmethod
    def create(cls, content_type, filename, file):
        rf = cls(content_type = content_type)
        rf.file.save(filename, file)
        return rf

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name_plural = "analyses"

@receiver(models.signals.post_delete, sender=Analysis)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding 'Analysis' object is deleted
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

    
