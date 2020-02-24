from django.shortcuts import render, redirect, reverse
from .forms import NewProductRequestForm
from .oktav_parts_later_delete_this import ProductRequest
from .models import ProductFeature, Widget
from django.http import HttpResponse

import json

# ezt le kell majd cserélni, minden productnak legyen sajátja
default_colorbar_dict = '{"color_scale":"alfa","minval":0,"maxval":8,"step_size":1,"bins":"None","color_count":9,"reverse":false}'

def home(request):
    return render(request, 'home.html')

def product_request(request):
    if request.method == 'POST':
        prf = NewProductRequestForm(request.POST)
        print(prf.errors)
        if prf.is_valid():

            get_colorbar_dict = request.POST.get('colorscale_colorbar_dict_extra')
            if get_colorbar_dict == 'NA':
                cscale = default_colorbar_dict
            else:
                cscale = get_colorbar_dict
            
            visual_settings = {
                'colorscale': json.loads(cscale),
                'figsize_x': 30, 'figsize_y': 17, 'dpi': 300,
                'rivers': request.POST.get('rivers_extra'),
                'municipality_borders': request.POST.get('municipality_borders_extra'),
                'state_borders': request.POST.get('state_borders_extra'),
                'country_borders': request.POST.get('country_borders_extra'), 
                'hillshade': request.POST.get('hillshade_extra'),
                'linediagram_grid': request.POST.get('linediagram_grid_extra'),
                'smooth': request.POST.get('smooth_extra'),
                'infobox': request.POST.get('infobox_extra'),
                'boxplot': request.POST.get('boxplot_extra'),
                'title': request.POST.get('title_extra'),
                'secondary_y_axis': request.POST.get('secondary_y_axis_extra')
                }

            print(visual_settings)

            PR = ProductRequest(
                product_type = request.POST.get('product_type'),
                parameter = request.POST.get('parameter'),
                aggregation_period = request.POST.get('aggregation_period'),
                season = request.POST.get('season'),
                scenario = request.POST.get('scenario'),
                region_option = request.POST.get('region_option'),
                region = request.POST.get('region'),
                period = [request.POST.get('period_start'), request.POST.get('period_end')],
                reference_period = [request.POST.get('reference_period_start'), request.POST.get('reference_period_end')],
                lower_height_filter = request.POST.get('lower_height_filter'),
                upper_height_filter = request.POST.get('upper_height_filter'),
                visual_settings = visual_settings,
                output_path = request.POST.get('output_path'),
                output_type = request.POST.get('output_type')
            )
            #print(PR)
            #func = getattr(PR, product_catalog[PR.product_type]['function'))
            #func()
            
            return redirect(reverse('product_result'))
        else:
            print('invalid')
    else:
        prf = NewProductRequestForm()
        return render(request, 'products.html', {'product_form': prf})

def product_result(request):
    return render(request, 'product_result.html')

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
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def get_queryset_attribute_values(qset, attr='name'):
    qlist = []
    for e in qset:
        qlist.append(getattr(e, attr))

    return ','.join([q for q in qlist])

def get_static_file(request):
    if True: #request.is_ajax():
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
