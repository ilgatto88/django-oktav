from django.shortcuts import render, redirect, reverse
from .forms import NewProductRequestForm
from .oktav_parts_later_delete_this import ProductRequest

def home(request):
    return render(request, 'home.html')

def product_request(request):
    if request.method == 'POST':
        prf = NewProductRequestForm(request.POST)
        colorbar_dict = request.POST.get('colorbar_dict')
        print(colorbar_dict)
        print(prf.errors)
        if prf.is_valid():
            visual_settings = {
                'colorscale': colorbar_dict,
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
            print(PR)
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

