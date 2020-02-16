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
        #widgets = Widget.objects.all()
        #widget_names = get_queryset_attribute_values(widgets, 'name')
        #print(widget_names)
        return render(request, 'products.html', {'product_form': prf}) #, 'widgets': widget_names

def product_result(request):
    return render(request, 'product_result.html')

def index(request):
    return render(request, 'index.html')

def fetch_product_features(request):
    if True: #request.is_ajax():
        q = request.GET.get('product_name', '')
        field = request.GET.get('field', '')

        selected_product = ProductFeature.objects.filter(name = q)[0]
        attribute_values = getattr(selected_product, field)
        widget_list = attribute_values.split(',')
        print(widget_list)
        widget_dict = {}
        for w in widget_list:
            print(w)
            widget_object =  Widget.objects.filter(name = w)[0]
            w_inner_dict = {}
            w_inner_dict['name'] = widget_object.name
            w_inner_dict['label'] = widget_object.label
            widget_dict[w] = w_inner_dict

        print(widget_dict)


        result = {field: attribute_values}
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
