from django.db import models

# Create your models here.
class ProductRequest(models.Model):
    product_type = models.CharField(max_length=40)
    parameter = models.CharField(max_length=30)
    parameter2 = models.CharField(max_length=30)
    aggregation_period = models.CharField(max_length=20)
    season = models.CharField(max_length=20)
    scenario = models.CharField(max_length=20)
    region_option = models.CharField(max_length=20)
    region = models.CharField(max_length=1000)
    period_start = models.IntegerField(blank=False)
    period_end = models.IntegerField(blank=False)
    reference_period_start = models.IntegerField()
    reference_period_end = models.IntegerField()
    lower_height_filter = models.IntegerField()
    upper_height_filter = models.IntegerField()
    output_path = models.CharField(max_length=255)
    output_type = models.CharField(max_length=20)
    visual_settings = models.CharField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_type + ', created at: ' + str(self.created_at)


class ProductVisualSettings(models.Model):
    colorscale = models.CharField(max_length=200)
    rivers = models.BooleanField(default=False)
    municipality_borders = models.BooleanField(default=False)
    state_borders = models.BooleanField(default=False)
    country_borders = models.BooleanField(default=False)
    hillshade = models.BooleanField(default=False)
    linediagram_grid = models.BooleanField(default=False)
    smooth = models.BooleanField(default=False)
    infobox = models.BooleanField(default=False)
    boxplot = models.BooleanField(default=False)
    title = models.BooleanField(default=False)
    secondary_y_axis = models.BooleanField(default=False)

    product_request = models.ForeignKey(ProductRequest, on_delete = models.CASCADE, related_name='visualsettings')

    def to_string(self):
        vis_set_text = {
            'colorscale': self.colorscale,
            'rivers': self.rivers,
            'municipality_borders': self.municipality_borders,
            'state_borders': self.state_borders,
            'country_borders': self.country_borders,
            'hillshade': self.hillshade,
            'linediagram_grid': self.linediagram_grid,
            'smooth': self.smooth,
            'infobox': self.infobox,
            'boxplot': self.boxplot,
            'title': self.title,
            'secondary_y_axis': self.secondary_y_axis
            }
        return str(vis_set_text)

class ColorScale(models.Model):
    name = models.CharField(max_length=50)
    minval = models.DecimalField(default=-99999.9, max_digits=9, decimal_places=1)
    maxval = models.DecimalField(default=99999.9, max_digits=9, decimal_places=1)
    step_size = models.DecimalField(default=0.0, max_digits=9, decimal_places=1)
    bins = models.IntegerField(default=0)
    color_count = models.IntegerField(default=0)
    reverse = models.BooleanField(default=False)

    visual_settings = models.ForeignKey(ProductVisualSettings, on_delete = models.CASCADE, related_name='colorscale_dict')

    def to_string(self):
        cscale_text = {
            'name': self.name,
            'minval': self.minval,
            'maxval': self.maxval,
            'step_size': self.step_size,
            'bins': self.bins,
            'color_count': self.color_count,
            'reverse': self.reverse
        }
        return str(cscale_text)

