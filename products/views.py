from django.shortcuts import render, redirect, reverse
from .forms import NewProductRequestForm
from oktav.products.product_processing import ProductRequest
from oktav.visualization.vis import createMapColors
from oktav.utils import importObject
from .models import ProductFeature, Widget, Season, Analysis, OutputType
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

def product_request(request):#, status, pk):
    if request.method == 'POST':
        prf = NewProductRequestForm(request.POST)
        print(prf.errors)
        #print(request.POST)
        if prf.is_valid():

            ########## visual settings ##########
            get_colorbar_dict = request.POST.get('colorscale_colorbar_dict_extra')
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

            product_settings = ProductFeature.objects.filter(name=request.POST.get('product_type'))[0]
            product_second_param = product_settings.has_second_parameter
            product_extras = ast.literal_eval(product_settings.extra)

            visual_settings = {
                'colorscale': extended_cscale,
                'figsize_x': product_extras['figsize_x'], 'figsize_y': product_extras['figsize_y'], 'dpi': product_extras['dpi'],
                'rivers': request.POST.get('rivers_extra') == 'on',
                'municipality_borders': request.POST.get('municipality_borders_extra') == 'on',
                'state_borders': request.POST.get('state_borders_extra') == 'on',
                'country_borders': request.POST.get('country_borders_extra') == 'on', 
                'hillshade': request.POST.get('hillshade_extra') == 'on',
                'linediagram_grid': request.POST.get('linediagram_grid_extra') == 'on',
                'smooth': request.POST.get('smooth_extra') == 'on',
                'infobox': request.POST.get('infobox_extra') == 'on',
                'boxplot': request.POST.get('boxplot_extra') == 'on',
                'title': request.POST.get('title_extra') == 'on',
                'secondary_y_axis': request.POST.get('secondary_y_axis_extra') == 'on'
                }
            ################################

            ########## 2nd parameter ##########
            if product_second_param:
                param = [request.POST.get('parameter'), request.POST.get('parameter2')]
            else:
                param = request.POST.get('parameter')
            ################################

            ########## season ##########
            if request.POST.get('aggregation_period') == 'YS':
                datum_start = '-01-01'
                datum_end = '-01-01'
            elif request.POST.get('aggregation_period') == 'QS-DEC':
                obj = Season.objects.filter(name=request.POST.get('season'))[0]
                datum_start = getattr(obj, 'datum_start')
                datum_end = getattr(obj, 'datum_end')
            ################################


            ########## region ##########
            region = ['austria'] if request.POST.get('region_option') == 'austria' else (request.POST.get('region')[0:-2]).replace(" ", "").split(",")
            if request.POST.get('region_option') == 'municipality':
                region_list = []
                a = Municipality.objects.all()[0]
                for i in region:
                    region_list.append(str(Municipality.objects.filter(name=i)[0].gkz))
            else:
                region_list = region

            ################################


            ########## height filters ##########
            lhf_from_html = request.POST.get('lower_height_filter')
            uhf_from_html = request.POST.get('upper_height_filter')
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
            if 'reference_period_checkbox' in request.POST.keys():
                if request.POST.get('reference_period_checkbox') != 'on':
                    refper = None
                else:
                    refper = [
                        request.POST.get('reference_period_start')+datum_start,
                        request.POST.get('reference_period_end')+datum_end
                        ]
            else:
                refper = None
            ################################

            PR = ProductRequest(
                product_type = request.POST.get('product_type'),
                parameter = param,
                aggregation_period = request.POST.get('aggregation_period'),
                season = request.POST.get('season'),
                scenario = [request.POST.get('scenario')],
                region_option = request.POST.get('region_option'),
                region = region_list,
                period = [request.POST.get('period_start')+datum_start, request.POST.get('period_end')+datum_end],
                reference_period = refper,
                lower_height_filter = adj_lower_height_filter,
                upper_height_filter = adj_upper_height_filter,
                visual_settings = visual_settings,
                output_path = request.POST.get('output_path'),
                output_type = request.POST.get('output_type'),
                django = True,
                django_path = settings.BASE_DIR + '/media/'
            )
            #print(PR.__dict__)
            product_func = ProductFeature.objects.filter(name = PR.product_type)[0].function
            func = getattr(PR, product_func)

            otype = OutputType.objects.filter(name = PR.output_type)[0].otype
            ofilename = PR.outname.split('/')[-1]
            def_filename = settings.MEDIA_ROOT + '/' + ofilename

            analysis = Analysis(content_type = otype, filename = ofilename, analysis_details = PR)
            func()
            
            analysis.file.save(def_filename, File(open(def_filename, 'rb')))
            analysis.file.name = ofilename
            analysis.save()
            
            #print(request.POST)
            return HttpResponseRedirect(reverse('analysis_result', args=(analysis.id,)))
    else:
        #if 'new' in str(request):
        prf = NewProductRequestForm()
        return render(request, 'products.html', {'product_form': prf})
        #else:
        #pass

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

def download(request, pk):
    analysis = get_object_or_404(Analysis, pk = pk)
    file = analysis.file
    return FileResponse(file, as_attachment=True, filename=file.name)