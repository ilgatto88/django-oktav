window.onload = function(){
    document.getElementById("colorbar_generate_button").onclick = createColorBarDict;
    document.getElementById("id_reference_period_checkbox").onchange = enableReferencePeriodFields;
    document.getElementById("id_region_option").onchange = enableRegionField;
    document.getElementById("id_aggregation_period").onchange = enableSeasonField;
    document.getElementById("id_product_type").onchange = enableParameter2Field;
    document.getElementById("collapse_button").onclick = changeParagraphSizeOnCollapse;
};

// This function enlarges or shrinks the paragraph based on it's actual size, connected to a button
function changeParagraphSizeOnCollapse() {
    empty_field = document.getElementById("empty-black-space");

    if (empty_field.style.height == "400px") {
        empty_field.style.height = "0px";
    } else {
        empty_field.style.height = "400px";
    }
}

// This function enables and disables the 2nd parameter drop-down menu based on the product name
function enableParameter2Field() {
    product_name = document.getElementById("id_product_type").value
    parameter2_field = document.getElementById("id_parameter2")
    if (product_name == 'product2') {
        parameter2_field.disabled = false;
    } else {
        parameter2_field.disabled = true;
    }
}

// This function enables and disables the season field based on the aggregation_period field
function enableSeasonField() {
    aggregation_period_value = document.getElementById("id_aggregation_period").value;
    if (aggregation_period_value == 'YS') {
        document.getElementById("id_season").disabled = true;
    } else {
        document.getElementById("id_season").disabled = false;
    }
}

// This function enables and disables the region field based on the region_option field
function enableRegionField() {
    region_option_value = document.getElementById("id_region_option").value;
    if (region_option_value == 'austria') {
        document.getElementById("id_region").disabled = true;
    } else {
        document.getElementById("id_region").disabled = false;
    }
}

// This function enables and disables the reference period fields based on the checkbox's state
function enableReferencePeriodFields() {
    checkbox_state = document.getElementById("id_reference_period_checkbox").checked
    if (checkbox_state) {
        document.getElementById("id_reference_period_start").disabled = false;
        document.getElementById("id_reference_period_end").disabled = false;
    } else {
        document.getElementById("id_reference_period_start").disabled = true;
        document.getElementById("id_reference_period_end").disabled = true;
    }
}

// This function creates a dictionary for the colorbar using the form fields of the document
function createColorBarDict() {
    colorscale = document.getElementById("id_colorscale_name_extra").value;
    minval = parseFloat(document.getElementById("id_colorscale_minval_extra").value);
    step_size = parseFloat(document.getElementById("id_colorscale_step_size_extra").value);
    reverse = document.getElementById("id_colorscale_reverse_extra").checked;

    color_count = 8; // needs to be changed!!

    if (step_size != 0.0) {
        if (step_size > 0) {
            var new_min = minval;
            var new_max = new_min + (color_count * step_size);
        } else {
            var new_min = minval + (color_count * step_size);
            var new_max = minval;
        }

        colorbar_dict = {
            'color_scale': colorscale,
            'minval': new_min,
            'maxval': new_max,
            'step_size': step_size,
            'bins': 'None',
            'color_count': color_count + 1,
            'reverse': reverse
        }

        // console.log(return_value);
        document.getElementById("id_colorscale_colorbar_dict_extra").value = JSON.stringify(colorbar_dict);
    } else {
        alert("Step size is zero!")
    }
}
