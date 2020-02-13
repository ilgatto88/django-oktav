from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Button, Fieldset, HTML, Div
from crispy_forms.bootstrap import FormActions, StrictButton

class NewProductRequestForm(forms.Form):
    # Choices
    PRODUCT_TYPE_CHOICES = (('product1', 'Product #1'), ('product2', 'Product #2'))
    PARAMETER_CHOICES = (('parameter1', 'Parameter #1'), ('parameter2', 'Parameter #2'))
    AGGRETATION_PERIOD_CHOICES = (('YS', 'Yearly'), ('QS-DEC', 'Seasonal'))
    SEASON_CHOICES = (('DJF', 'Winter'), ('MAM', 'Spring'), ('JJA', 'Summer'), ('SON', 'Autumn'))
    SCENARIO_CHOICES = (('rcp26', 'RCP2.6'), ('rcp45', 'RCP4.5'), ('rcp85', 'RCP8.5'))
    REGION_OPTION_CHOICES = (('austria', 'Austria'), ('bundesland', 'Bundesland'), ('gemeinde', 'Municipality'))
    OUTPUT_TYPE_CHOICES = (('pdf', 'PDF'), ('png', 'PNG'), ('txt', 'TXT'))
    BASE_OUTPUT_PATH = '/home/jtordai/Desktop/'

    # Product settings
    product_type = forms.ChoiceField(label='Product type', choices=PRODUCT_TYPE_CHOICES)
    parameter = forms.ChoiceField(label='Parameter', choices=PARAMETER_CHOICES)
    parameter2 = forms.ChoiceField(label='2nd parameter', choices=PARAMETER_CHOICES, required=False)
    aggregation_period = forms.ChoiceField(label='Aggregation period', choices=AGGRETATION_PERIOD_CHOICES)
    season = forms.ChoiceField(label='Season', choices=SEASON_CHOICES, required=False, disabled=True)
    scenario = forms.ChoiceField(label='Scenario', choices=SCENARIO_CHOICES, required=False)
    region_option = forms.ChoiceField(label='Region option', choices=REGION_OPTION_CHOICES)
    region = forms.CharField(label='Region(s)', max_length=1000, required=False, disabled=True)

    period_start = forms.IntegerField(label='Period start', initial=2021)
    period_end = forms.IntegerField(label='Period end', initial=2050)
    reference_period_checkbox = forms.BooleanField(label="", required=False, initial=True)
    reference_period_start = forms.IntegerField(label='Reference period', initial=1971, required=False)
    reference_period_end = forms.IntegerField(label='', initial=2000, required=False)
    lower_height_filter = forms.IntegerField(label='Lower height filter (m)', initial=0, required=False)
    upper_height_filter = forms.IntegerField(label='Upper height filter (m)', initial=0, required=False)

    output_path = forms.CharField(label='Output path', initial=BASE_OUTPUT_PATH)
    output_type = forms.ChoiceField(label='Output type', choices=OUTPUT_TYPE_CHOICES)

    # Extra product settings
    COLORBAR_CHOICES = (('alfa', 'alfa'), ('bravo', 'bravo'))
    ## Colorscale
    colorscale_name_extra = forms.ChoiceField(label="Colorscale", required=False, choices=COLORBAR_CHOICES)
    colorscale_minval_extra = forms.DecimalField(label="First value", initial=0.0, max_digits=9, decimal_places=1, required=False)
    colorscale_step_size_extra = forms.DecimalField(label="Step size", initial=0.0, max_digits=9, decimal_places=1, required=False)
    colorscale_reverse_extra = forms.BooleanField(label="Reverse", initial=False, required=False)
    colorscale_colorbar_dict_extra = forms.CharField(label="Colorbar", max_length=200, required = False, initial='NA')

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

