window.onload = function(){
    document.getElementById("colorbar_generate_button").onclick = createColorBarDict;
};

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

    // console.log(colorbar_dict);
    return colorbar_dict
}
