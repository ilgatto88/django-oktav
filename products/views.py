from django.shortcuts import render
from .forms import NewProductRequestForm
from .oktav_parts_later_delete_this import ProductRequest

def product_request(request):
    if request.method == 'POST':
        print('this is POST')
        prf = NewProductRequestForm(request.POST)
        if prf.is_valid():
            print('is valid')
            PR = ProductRequest(
                product_type = prf['product_type'],
                parameter = prf['parameter'],
                aggregation_period = prf['aggregation_period'],
                season = prf['season'],
                scenario = prf['scenario'],
                region_option = prf['region_option'],
                region = prf['region'],
                period = [prf['period_start'], prf['period_end']],
                reference_period = [prf['reference_period_start'], prf['reference_period_end']],
                lower_height_filter = prf['lower_height_filter'],
                upper_height_filter = prf['upper_height_filter'],
                visual_settings = prf['visual_settings'],
                output_path = prf['output_path'],
                output_type = prf['output_type']
            )

            print(PR)
            #func = getattr(PR, product_catalog[PR.product_type]['function'])
            #func()
            return redirect('generating_product')
        else:
            print('not valid')
    else:
        prf = NewProductRequestForm()
        print('this is GET')
        return render(request, 'products.html', {'prf': prf})
