from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Button, Fieldset, HTML, Div
from crispy_forms.bootstrap import FormActions, StrictButton

class NewProductRequestForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(NewProductRequestForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Generate'))
        self.helper.layout = Layout(
            'product_type',
            'parameter',
            'aggregation_period',
            'season',
            'scenario',
            'region_option',
            'region',
            'period_start',
            'period_end',
            'reference_period_start',
            'reference_period_end',
            'lower_height_filter',
            'upper_height_filter',
            'output_path',
            'output_type',
            'visual_settings'
        )

    PRODUCT_TYPE_CHOICES = (('Product #1', 'product1'), ('Product #2', 'product2'))
    PARAMETER_CHOICES = (('Parameter #1', 'parameter1'), ('Parameter #2', 'parameter2'))
    AGGRETATION_PERIOD_CHOICES = (('yearly', 'YS'), ('seasonal', 'QS-DEC'))
    SEASON_CHOICES = (('Winter', 'DJF'), ('Spring', 'MAM'), ('Summer', 'JJA'), ('Autumn', 'SON'))
    SCENARIO_CHOICES = (('RCP2.6', 'rcp26'), ('RCP4.5', 'rcp45'), ('RCP8.5', 'rcp85'))
    REGION_OPTION_CHOICES = (('Austria', 'austria'), ('Bundesland', 'bundesland'), ('Municipality', 'gemeinde'))
    OUTPUT_TYPE_CHOICES = (('pdf', 'pdf'), ('png', 'png'), ('txt', 'txt'))
    BASE_OUTPUT_PATH = '/home/jtordai/Desktop/'


    product_type = forms.ChoiceField(label='Product type', choices=PRODUCT_TYPE_CHOICES)
    parameter = forms.ChoiceField(label='Parameter', choices=PARAMETER_CHOICES)
    parameter2 = forms.ChoiceField(label='2nd parameter', choices=PARAMETER_CHOICES, required=False)
    aggregation_period = forms.ChoiceField(label='Aggregation period', choices=AGGRETATION_PERIOD_CHOICES)
    season = forms.ChoiceField(label='Season', choices=SEASON_CHOICES)
    scenario = forms.ChoiceField(label='Scenario', choices=SCENARIO_CHOICES)
    region_option = forms.ChoiceField(label='Region option', choices=REGION_OPTION_CHOICES)
    region = forms.CharField(label='Region(s)', max_length=1000)

    period_start = forms.IntegerField(label='Period start', initial=2021)
    period_end = forms.IntegerField(label='Period end', initial=2050)
    reference_period_start = forms.IntegerField(label='Reference period start', initial=1971)
    reference_period_end = forms.IntegerField(label='Reference period end', initial=2000)
    lower_height_filter = forms.IntegerField(label='Lower height filter', initial=0)
    upper_height_filter = forms.IntegerField(label='Upper height filter', initial=0)

    output_path = forms.CharField(label='Output path', initial=BASE_OUTPUT_PATH)
    output_type = forms.ChoiceField(label='Output type', choices=OUTPUT_TYPE_CHOICES)
    visual_settings = forms.CharField(label='Visual settings', max_length=1000)

class NewProductVisualSettings(forms.Form):
    colorscale = forms.CharField(max_length=200)
    rivers = forms.BooleanField(initial=False)
    municipality_borders = forms.BooleanField(initial=False)
    state_borders = forms.BooleanField(initial=False)
    country_borders = forms.BooleanField(initial=False)
    hillshade = forms.BooleanField(initial=False)
    linediagram_grid = forms.BooleanField(initial=False)
    smooth = forms.BooleanField(initial=False)
    infobox = forms.BooleanField(initial=False)
    boxplot = forms.BooleanField(initial=False)
    title = forms.BooleanField(initial=False)
    secondary_y_axis = forms.BooleanField(initial=False)

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

class NewColorScale(forms.Form):
    name = forms.CharField(max_length=50)
    minval = forms.DecimalField(initial=0.0, max_digits=9, decimal_places=1)
    maxval = forms.DecimalField(initial=0.0, max_digits=9, decimal_places=1)
    step_size = forms.DecimalField(initial=0.0, max_digits=9, decimal_places=1)
    bins = forms.IntegerField(initial=0)
    color_count = forms.IntegerField(initial=0)
    reverse = forms.BooleanField(initial=False)

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
