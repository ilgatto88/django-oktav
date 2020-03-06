from django.shortcuts import render, redirect, reverse
from .forms import NewProductRequestForm
from oktav.products.product_processing import ProductRequest
from oktav.visualization.vis import createMapColors
from oktav.utils import importObject
from .models import ProductFeature, Widget, Season, Analysis, OutputType, AggregationPeriod
from region.models import Municipality
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.views.generic.edit import DeleteView
from django.conf import settings
from django.core.files.storage import File
import django

import json
import ast

default_colorbar_dict = '{"color_scale":"alfa","minval":-20,"maxval":35,"step_size":1,"bins":"None","color_count":56,"reverse":false}'

def home(request):
    return render(request, 'home.html')

def requestPOSTFunction(request_post):
    prf = NewProductRequestForm(request_post)
    print(prf.errors)
    print(request_post)
    if prf.is_valid():

        ########## visual settings ##########
        get_colorbar_dict = request_post.get('colorscale_colorbar_dict_extra')
        cscale = default_colorbar_dict if get_colorbar_dict == '' else get_colorbar_dict
        cscale_loaded = json.loads(cscale)
        cscale_loaded['bins'] = None if cscale_loaded['bins'] == 'None' else cscale_loaded['bins']

        extended_cscale = createMapColors(
            color_scale = cscale_loaded['color_scale'],
            minval = cscale_loaded['minval'],
            maxval= cscale_loaded['maxval'],
            step_size = cscale_loaded['step_size'],
            bins = cscale_loaded['bins'],
            color_count = cscale_loaded['color_count'],
            reverse = cscale_loaded['reverse'])

        product_settings = ProductFeature.objects.filter(name=request_post.get('product_type'))[0]
        product_second_param = product_settings.has_second_parameter
        product_extras = ast.literal_eval(product_settings.extra)

        visual_settings = {
            'colorscale': extended_cscale,
            'figsize_x': product_extras['figsize_x'], 'figsize_y': product_extras['figsize_y'], 'dpi': product_extras['dpi'],
            'rivers': request_post.get('rivers_extra') == 'on',
            'municipality_borders': request_post.get('municipality_borders_extra') == 'on',
            'state_borders': request_post.get('state_borders_extra') == 'on',
            'country_borders': request_post.get('country_borders_extra') == 'on', 
            'hillshade': request_post.get('hillshade_extra') == 'on',
            'linediagram_grid': request_post.get('linediagram_grid_extra') == 'on',
            'smooth': request_post.get('smooth_extra') == 'on',
            'infobox': request_post.get('infobox_extra') == 'on',
            'boxplot': request_post.get('boxplot_extra') == 'on',
            'title': request_post.get('title_extra') == 'on',
            'secondary_y_axis': request_post.get('secondary_y_axis_extra') == 'on'
            }
        ################################

        ########## 2nd parameter ##########
        if product_second_param:
            param = [request_post.get('parameter'), request_post.get('parameter2')]
        else:
            param = request_post.get('parameter')
        ################################

        ########## season ##########
        if request_post.get('aggregation_period') == 'YS':
            datum_start = '-01-01'
            datum_end = '-01-01'
        elif request_post.get('aggregation_period') == 'QS-DEC':
            obj = Season.objects.filter(name=request_post.get('season'))[0]
            datum_start = getattr(obj, 'datum_start')
            datum_end = getattr(obj, 'datum_end')
        ################################


        ########## region ##########
        if request_post.get('region_option') == 'austria': # austria
            region = ['austria']
        else: # bundesland, municipality
            region_a = (request_post.get('region')[0:-2]).split(",")
            region = [a.lstrip() for a in region_a]

        if request_post.get('region_option') == 'municipality':
            region_list = []
            for i in region:
                region_list.append(str(Municipality.objects.filter(name=i)[0].gkz))
        else:
            region_list = region

        ################################


        ########## height filters ##########
        lhf_from_html = request_post.get('lower_height_filter')
        uhf_from_html = request_post.get('upper_height_filter')
        if uhf_from_html == '0':
            adj_upper_height_filter = None
            if lhf_from_html == '0':
                adj_lower_height_filter = None
            else:
                adj_lower_height_filter = int(lhf_from_html)
        else:
            adj_upper_height_filter = int(uhf_from_html)
            if lhf_from_html == '0':
                adj_lower_height_filter = 0
            else:
                adj_lower_height_filter = int(lhf_from_html)
        ################################


        ########## reference period ##########
        if 'reference_period_checkbox' in request_post.keys():
            if request_post.get('reference_period_checkbox') != 'on':
                refper = None
                refper_checkbox_for_settings = "off"
            else:
                refper_checkbox_for_settings = "on"
                refper = [
                    request_post.get('reference_period_start')+datum_start,
                    request_post.get('reference_period_end')+datum_end
                    ]
        else:
            refper_checkbox_for_settings = "off"
            refper = None
        ################################

        PR = ProductRequest(
            product_type = request_post.get('product_type'),
            parameter = param,
            aggregation_period = request_post.get('aggregation_period'),
            season = request_post.get('season'),
            scenario = [request_post.get('scenario')],
            region_option = request_post.get('region_option'),
            region = region_list,
            period = [request_post.get('period_start')+datum_start, request_post.get('period_end')+datum_end],
            reference_period = refper,
            lower_height_filter = adj_lower_height_filter,
            upper_height_filter = adj_upper_height_filter,
            visual_settings = visual_settings,
            output_path = request_post.get('output_path'),
            output_type = request_post.get('output_type'),
            django = True,
            django_path = settings.BASE_DIR + '/media/'
        )
        #print(PR.__dict__)
        product_func = ProductFeature.objects.filter(name = PR.product_type)[0].function
        func = getattr(PR, product_func)

        otype = OutputType.objects.filter(name = PR.output_type)[0].otype
        ofilename = PR.outname.split('/')[-1]
        def_filename = settings.MEDIA_ROOT + '/' + ofilename

        ################## settings dictionary ##################x

        
        if region[0] == 'austria':
            region_list_for_settings = ''
        else:
            region_list_for_settings = (', ').join(region)

        
        if request_post.get('aggregation_period') == 'YS':
            season_for_settings = "DJF"
        else:
            season_for_settings = request_post.get('season')
        
        settings_dict = {
            "id_product_type": request_post.get('product_type'),
            "id_scenario": request_post.get('scenario'),
            "id_parameter": request_post.get('parameter'),
            "id_parameter2": request_post.get('parameter2'),
            "id_aggregation_period": request_post.get('aggregation_period'),
            "id_season": season_for_settings,
            "id_region_option": request_post.get('region_option'),
            "id_region": region_list_for_settings,
            "id_period_start": request_post.get('period_start'),
            "id_period_end": request_post.get('period_end'),
            "id_reference_period_checkbox": refper_checkbox_for_settings,
            "id_reference_period_start": request_post.get('reference_period_start'),
            "id_reference_period_end": request_post.get('reference_period_end'),
            "id_lower_height_filter": request_post.get('lower_height_filter'),
            "id_upper_height_filter": request_post.get('upper_height_filter'),
            "id_output_type": request_post.get('output_type'),
            "id_output_path": request_post.get('output_path'),
            "id_colorscale_colorbar_dict_extra": request_post.get('colorscale_colorbar_dict_extra'),
            "id_colorscale_name_extra": cscale_loaded['color_scale'],
            "id_colorscale_minval_extra": cscale_loaded['minval'],
            "id_colorscale_step_size_extra": cscale_loaded['step_size'],
            "id_colorscale_reverse_extra": cscale_loaded['reverse'],
            "id_rivers_extra": request_post.get('rivers_extra'),
            "id_municipality_borders_extra": request_post.get('municipality_borders_extra'),
            "id_state_borders_extra": request_post.get('state_borders_extra'),
            "id_country_borders_extra": request_post.get('country_borders_extra'),
            "id_hillshade_extra": request_post.get('hillshade_extra'),
            "id_linediagram_grid_extra": request_post.get('linediagram_grid_extra'),
            "id_smooth_extra": request_post.get('smooth_extra'),
            "id_infobox_extra": request_post.get('infobox_extra'),
            "id_boxplot_extra": request_post.get('boxplot_extra'),
            "id_title_extra": request_post.get('title_extra'),
            "id_secondary_y_axis_extra": request_post.get('secondary_y_axis_extra')
        }


        analysis = Analysis(content_type = otype, filename = ofilename, analysis_details = PR, settings_json = json.dumps(settings_dict))
        func()
        
        analysis.file.save(def_filename, File(open(def_filename, 'rb')))
        analysis.file.name = ofilename
        analysis.save()
        
        #print(request.POST)
        return analysis.id


def product_request(request):
    if request.method == 'POST':
        id = requestPOSTFunction(request_post = request.POST)
        return HttpResponseRedirect(reverse('analysis_result', args=(id,)))
    else:
        prf = NewProductRequestForm()
        return render(request, 'products.html', {'product_form': prf})

def product_request_refine(request, pk):
    if request.method == 'POST':
        id = requestPOSTFunction(request_post = request.POST)
        return HttpResponseRedirect(reverse('analysis_result', args=(id,)))
    else:
        prf = NewProductRequestForm()
        return render(request, 'products.html', {'product_form': prf, 'analysis_id': pk})

def analysis_result(request, pk):
    analysis = get_object_or_404(Analysis, pk = pk)
    return render(request, 'analysis_result.html', {'analysis': analysis})


class AnalysisDeleteView(DeleteView):
    model = Analysis
    template_name="analysis_confirm_delete.html"

    def get_success_url(self):
        return reverse('index')

def index(request):
    return render(request, 'index.html')

def fetch_product_features(request):
    if request.is_ajax():
        q = request.GET.get('product_name', '')
        field = request.GET.get('field', '')
        selected_product = ProductFeature.objects.filter(name = q)[0]
        attrs_to_remove = ['_state', 'id']
        if field == 'all':
            product_attributes = list(selected_product.__dict__.keys())
            product_attributes = [ele for ele in product_attributes if ele not in attrs_to_remove]
            product_feature_dict = {}
            for attr in product_attributes:
                product_feature_dict[attr] = getattr(selected_product, attr)
            data = json.dumps(product_feature_dict)
        elif field == 'widgets':
            attribute_values = getattr(selected_product, field)
            if attribute_values != 'None':
                widget_list = attribute_values.split(',')
                widget_dict = {}
                for w in widget_list:
                    widget_object =  Widget.objects.filter(name = w)[0]
                    widget_attributes = list(widget_object.__dict__.keys())
                    widget_attributes = [ele for ele in widget_attributes if ele not in attrs_to_remove]
                    w_inner_dict = {}
                    for wattr in widget_attributes:
                        w_inner_dict[wattr] = getattr(widget_object, wattr)
                        widget_dict[w] = w_inner_dict

                result = {field: widget_dict}
                data = json.dumps(result)
            else:
                data = json.dumps({"widgets": {"None": "None"}})
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def get_queryset_attribute_values(qset, attr='name'):
    qlist = []
    for e in qset:
        qlist.append(getattr(e, attr))

    return ','.join([q for q in qlist])

def get_static_file(request):
    if request.is_ajax():
        rfile = request.GET.get('file', '')
        with open(rfile) as json_file:
            data = json.load(json_file)
        
        res = json.dumps(data)
    else:
        res = 'fail'
    mimetype = 'application/json'
    return HttpResponse(res, mimetype)

def get_enabled_parameters_by_aggp(request):
    if request.is_ajax():
        aggp_type = request.GET.get('aggp_type', '')
        aggp = AggregationPeriod.objects.filter(name=aggp_type)[0]
        data = aggp.enabled_parameters.split(',')
        data = json.dumps(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def documentation(request):
    return render(request, '_build/html/index.html')

def getModelObjects(request):
    if request.is_ajax():
        model = request.GET.get('model', '').capitalize()
        obj = importObject(obj_name='products.models.' + model)
        all_objs = obj.objects.all()
        d = {}
        odict = {}
        for o in all_objs:
            odict = {o.name: {'name': o.name, 'enabled': o.enabled}}
            d.update(odict)

        result = {'objects': d}
        data = json.dumps(result)
    else:
        data = 'fail'
        
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def get_analysis_settings(request):
    if True: #request.is_ajax():
        analysis_id = request.GET.get('analysis_id', '')
        analysis = Analysis.objects.filter(id=analysis_id)[0]
        data = analysis.settings_json
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def download(request, pk):
    analysis = get_object_or_404(Analysis, pk = pk)
    file = analysis.file
    return FileResponse(file, as_attachment=True, filename=file.name)