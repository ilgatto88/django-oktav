import json
from django import forms
from django.forms import ModelForm

from .models import ProductFeature, Parameter, AggregationPeriod, Season
from .models import Scenario, RegionOption, OutputType

class NewProductRequestForm(forms.Form):
    # model requests
    product_queryset = ProductFeature.objects.all()
    parameter_queryset = Parameter.objects.all()
    aggregation_period_queryset = AggregationPeriod.objects.all()
    season_queryset = Season.objects.all()
    scenario_queryset = Scenario.objects.all()
    region_option_queryset = RegionOption.objects.all()
    output_type_queryset = OutputType.objects.all()

    # Choices
    ptype_pname = [[p.name, p.print_name] for p in product_queryset]
    PRODUCT_TYPE_CHOICES = [tuple(l) for l in ptype_pname]

    parameters = [[p.name, p.print_name] for p in parameter_queryset]
    PARAMETER_CHOICES = [tuple(l) for l in parameters]
    
    agg_periods = [[p.name, p.print_name] for p in aggregation_period_queryset]
    AGGRETATION_PERIOD_CHOICES = [tuple(l) for l in agg_periods]

    seasons = [[p.name, p.print_name] for p in season_queryset]
    SEASON_CHOICES = [tuple(l) for l in seasons]
    
    scenarios = [[p.name, p.print_name] for p in scenario_queryset]
    SCENARIO_CHOICES = [tuple(l) for l in scenarios]

    region_options = [[p.name, p.print_name] for p in region_option_queryset]
    REGION_OPTION_CHOICES = [tuple(l) for l in region_options]

    output_types = [[p.name, p.print_name] for p in output_type_queryset]
    OUTPUT_TYPE_CHOICES = [tuple(l) for l in output_types]
    
    BASE_OUTPUT_PATH = '/home/jtordai/Desktop/'

    # Product settings
    product_type = forms.ChoiceField(label='Product type', choices=PRODUCT_TYPE_CHOICES)
    parameter = forms.ChoiceField(label='Parameter', choices=PARAMETER_CHOICES)
    parameter2 = forms.ChoiceField(label='2nd parameter', choices=PARAMETER_CHOICES, required=False)
    aggregation_period = forms.ChoiceField(label='Aggregation period', choices=AGGRETATION_PERIOD_CHOICES)
    season = forms.ChoiceField(label='Season', choices=SEASON_CHOICES, required=False, disabled=True)
    scenario = forms.ChoiceField(label='Scenario', choices=SCENARIO_CHOICES, required=False)
    region_option = forms.ChoiceField(label='Region option', choices=REGION_OPTION_CHOICES)
    region = forms.CharField(
        label='Region(s)',
        max_length=1000,
        required=False,
        disabled=True,
        widget=forms.TextInput(attrs={'placeholder': "Start typing (2 letters needed)"})
        )

    period_start = forms.IntegerField(label='Period')
    period_end = forms.IntegerField(label='.')
    reference_period_checkbox = forms.BooleanField(label='Reference period', required=False, initial=True)
    reference_period_start = forms.IntegerField(label='.', initial=1971, required=False, min_value=1961, max_value=1981)
    reference_period_end = forms.IntegerField(label='.', initial=2000, required=False, min_value=1990, max_value=2010)
    lower_height_filter = forms.IntegerField(label='Lower height filter', initial=0, required=False, min_value=0, max_value=9999)
    upper_height_filter = forms.IntegerField(label='Upper height filter', initial=0, required=False, min_value=0, max_value=9999)

    output_path = forms.CharField(label='Output path', initial=BASE_OUTPUT_PATH)
    output_type = forms.ChoiceField(label='Output type', choices=OUTPUT_TYPE_CHOICES)

    # Extra product settings
    with open('products/static/colorscales.json') as json_file:
        data = json.load(json_file)

    cb_list = list(data)
    colorbars = [[p, p] for p in cb_list]
    COLORBAR_CHOICES = [tuple(l) for l in colorbars]

    ## Colorscale
    colorscale_name_extra = forms.ChoiceField(label="Colorscale", required=False, choices=COLORBAR_CHOICES)
    colorscale_minval_extra = forms.DecimalField(label="First value", initial=0.0, decimal_places=1, max_digits=6, required=False, max_value=99999, min_value=-99999)
    colorscale_step_size_extra = forms.DecimalField(label="Step size", initial=0.0, decimal_places=1, max_digits=6, required=False, max_value=99999, min_value=-99999)
    colorscale_reverse_extra = forms.BooleanField(label="Reverse", initial=False, required=False)
    colorscale_colorbar_dict_extra = forms.CharField(widget=forms.HiddenInput(), required=False)

    ## Additional checkboxes
    rivers_extra = forms.BooleanField(label="Rivers", initial=False, required=False)
    municipality_borders_extra = forms.BooleanField(label="Municipality borders", initial=False, required=False)
    state_borders_extra = forms.BooleanField(label="State borders", initial=False, required=False)
    country_borders_extra = forms.BooleanField(label="Country borders", initial=False, required=False)
    hillshade_extra = forms.BooleanField(label="Hillshade", initial=False, required=False)
    linediagram_grid_extra = forms.BooleanField(label="Grid", initial=False, required=False)
    smooth_extra = forms.BooleanField(label="Smooth", initial=False, required=False)
    infobox_extra = forms.BooleanField(label="Infobox", initial=False, required=False)
    boxplot_extra = forms.BooleanField(label="Boxplot", initial=False, required=False)
    title_extra = forms.BooleanField(label="Title", initial=False, required=False)
    secondary_y_axis_extra = forms.BooleanField(label="Secondary y-axis", initial=False, required=False)
