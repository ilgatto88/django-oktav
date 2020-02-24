window.onload = function(){
    document.getElementById("colorbar_generate_button").onclick = createColorBarDict;
    document.getElementById("id_reference_period_checkbox").onchange = enableReferencePeriodFields;
    document.getElementById("id_region_option").onchange = enableRegionField;
    document.getElementById("id_aggregation_period").onchange = enableSeasonField;
    document.getElementById("id_product_type").onchange = productTypeSettings;
    document.getElementById("collapse_button").onclick = collapseEvents;
    document.getElementById("id_colorscale_name_extra").onchange = changeColorscale;
    document.getElementById("colorbar_generate_button").onclick = reDrawColorBar;
};

function reDrawColorBar() {
    if (document.getElementById("colorbar_table").innerHTML.indexOf("table") != -1) {
        document.getElementById("colorbar_table").innerHTML = "";
    };
    createColorScaleTable( create_html_colordict(redraw=true) );
}

function changeColorscale() {
    if (document.getElementById("colorbar_table").innerHTML.indexOf("table") != -1) {
        document.getElementById("colorbar_table").innerHTML = "";
    };
    createColorScaleTable( create_html_colordict() );
};

// This function enlarges or shrinks the paragraph based on it's actual size, connected to a button
function collapseEvents() {

    // here we add some more space below extra settings
    empty_field = document.getElementById("empty-black-space");
    if (empty_field.style.height == "400px") {
        empty_field.style.height = "0px";
    } else {
        empty_field.style.height = "400px";
    };

    // here we add the extra buttons
    var field_collapsed = document.getElementById("collapse_button").getAttribute("aria-expanded");
    if (field_collapsed == "false") {
        var extra_settings_html = document.getElementById('extra_settings').innerHTML;
        if (extra_settings_html.indexOf("form-row") == -1) {
            createExtraSettingsCheckboxes( getProductFeatures(field_name = 'widgets') );
            };
        var colorbar_inner_html = document.getElementById('colorbar_table').innerHTML;
        if (colorbar_inner_html.indexOf("table") == -1) {
            createColorScaleTable( create_html_colordict() );
            };
        };
    };

function create_html_colordict(redraw=false) {

    var colorscales = JSON.parse(getStaticFile('products/static/colorscales.json'));
    var colors = JSON.parse(getStaticFile('products/static/colors.json'));

    var selected_colorscale = document.getElementById("id_colorscale_name_extra").value;
    var selected_colorscale_features = colorscales[selected_colorscale];
    var selected_colors = colors[selected_colorscale];

    if (redraw == true) {
        if (document.getElementById("id_colorscale_reverse_extra").checked == true) {
            var selected_colors = selected_colors.reverse()
        };
        var minval = parseFloat(document.getElementById("id_colorscale_minval_extra").value);
        console.log(minval);
        var step = parseFloat(document.getElementById("id_colorscale_step_size_extra").value);
        console.log(step);
        value_array = []
        for (var i = 0; i < selected_colors.length; i++) {
            val = (minval + (i*step)).toFixed(1);
            value_array.push(val);
        };
    } else {
        var minval = selected_colorscale_features["minval"];
        console.log(minval);
        var step = selected_colorscale_features["step"];
        console.log(step);
        document.getElementById("id_colorscale_minval_extra").value = minval;
        if (step != 'fixed') {
            document.getElementById("id_colorscale_step_size_extra").value = step;
            value_array = []
            for (var i = 0; i < selected_colors.length; i++) {
                val = (minval + (i*step)).toFixed(1);
                value_array.push(val);
            };
            
        } else {
            value_array = []
            for (var i = 0; i < selected_colors.length; i++) {
                value_array.push((selected_colorscale_features["bins"][i]).toFixed(1));
            };
        };
    };

    console.log(value_array);
    var colordict = {
        colors: colors[selected_colorscale],
        values: value_array
    };
    return colordict;
};

function getStaticFile(url, callback) {
    var file_contents = $.ajax({
        url: "/api/get_static_file/",
        type: "GET",
        async: false,
        dataType: 'json',
        data: {
            file : url
        }
    });
    return file_contents.responseText;
};

// This function adjust selectable settings in form based on the product name
function productTypeSettings() {

    // get product features
    var productFeatures = getProductFeatures(field_name = 'all', set_async = false);
    var parsed_productFeatures = JSON.parse(productFeatures);
    // enable scenario field
    var scenario_field = document.getElementById("id_scenario");
    var scenario_enabled = parsed_productFeatures['selectable_rcp'];
    if (scenario_enabled == true) {
        scenario_field.disabled = false;
    } else {
        scenario_field.disabled = true;
    };

    // 2nd parameter field
    var second_param_field_enabled = parsed_productFeatures['has_second_parameter'];
    var parameter2_field = document.getElementById("parameter2_div");
    if (second_param_field_enabled == true) {
        parameter2_field.style.visibility = "visible";
    } else {
        parameter2_field.style.visibility = "hidden";
    };

    // lock reference perid checkbox
    var product_must_have_reference_period = parsed_productFeatures['must_have_reference_period'];
    var ref_per_checkbox = document.getElementById("id_reference_period_checkbox");
    if (product_must_have_reference_period == true) {
        ref_per_checkbox.checked = true;
        ref_per_checkbox.disabled = true;
    } else {
        ref_per_checkbox.disabled = false;
        ref_per_checkbox.checked = true;
    }

    // enable/disable output types
    var output_type_field = document.getElementById("id_output_type");
    var output_count = output_type_field.options.length;
    var product_type_outputs = parsed_productFeatures['output_types'];
    for (i = 0; i < output_count; i++) {
        var mod_i = i.toString().concat(',');
        if (product_type_outputs.includes(mod_i) == true) {
            output_type_field.options[i].disabled = false;
        } else {
            output_type_field.options[i].disabled = true;
        };
      };

    // extra settings in collapsable area
    var extra_settings_field = document.getElementById('extra_settings');
    var field_collapsed = document.getElementById("collapse_button").getAttribute("aria-expanded");
    if (field_collapsed == "true") {
        extra_settings_field.innerHTML = "";
        createExtraSettingsCheckboxes(
            getProductFeatures(field_name = 'widgets')
            );
    } else {
        extra_settings_field.innerHTML = "";
    };
};

function getProductFeatures(field_name, set_async = false, callback) {
    var widgets_call_result = $.ajax({
      url: "/api/get_product_features/",
      type: "GET",
      async: set_async,
      dataType: 'json',
      data: {
        product_name : document.getElementById("id_product_type").value,
        field: field_name
      }
    });
    return widgets_call_result.responseText;
  };

function createColorScaleTable(colordict) {
    var colorBarDiv = document.getElementById("colorbar_table");
    var newTable = document.createElement("TABLE");
    newTable.classList.add("table");
    newTable.classList.add("colorbar_table");
    colorBarDiv.insertBefore(newTable, null)
    var tableRowColor = newTable.insertRow(0);
    var tableRowValue = newTable.insertRow(1);

    var colors = colordict['colors'];
    var colorCount = colors.length;
    var td_width = (1/colorCount).toString().concat('%')

    for (i = 0; i < colorCount; i++) {
        var newTableDataColor = tableRowColor.insertCell(i);
        newTableDataColor.style.backgroundColor = colors[i];
        newTableDataColor.style.width = td_width;
        newTableDataColor.style.height = '30px';
        newTableDataColor.style.padding = '0';

        var newTableDataValue = tableRowValue.insertCell(i);
        newTableDataValue.style.width = td_width;
        newTableDataValue.style.height = '10px';
        newTableDataValue.style.fontSize = '70%';
        newTableDataValue.style.padding = '0';
        if ((colorCount <= 10) || (colorCount > 10 && colorCount <= 30 && i%3 === 0) || (colorCount > 30 && i%5 === 0)) {
            newTableDataValue.innerHTML = colordict['values'][i].toString();
        };
    };
};

function createExtraSettingsCheckboxes(pc) {
    var product_checkboxes = JSON.parse(pc)['widgets'];
    for (var key in product_checkboxes) {
        if (product_checkboxes.hasOwnProperty(key)) {
            var newFormRowExtra = document.createElement("DIV");
            newFormRowExtra.classList.add("form-row");
            var newFormColExtra = document.createElement("DIV");
            newFormColExtra.classList.add("form-col");
            newFormColExtra.classList.add("col-lg-6");
            newFormColExtra.classList.add("ml-2")
            var newFormGroupExtra = document.createElement("DIV");
            newFormGroupExtra.classList.add("form-group");
            newFormGroupExtra.classList.add("mb-0")

            var checkbox_element = document.createElement("INPUT");
            var checkbox_element_name = product_checkboxes[key]['name'];
            var checkbox_element_label = product_checkboxes[key]['label'];
            var checkbox_element_id = 'id_'.concat(product_checkboxes[key]['name']);

            checkbox_element.setAttribute("type", "checkbox");
            checkbox_element.setAttribute("id", checkbox_element_id);
            checkbox_element.classList.add("oktav-dropdown");

            var checkbox_label_element = document.createElement("LABEL");
            checkbox_label_element.setAttribute("for", checkbox_element_id);
            checkbox_label_element.classList.add("text-nowrap");
            checkbox_label_element.classList.add("ml-2");
            var checkbox_label_element_text = document.createTextNode(checkbox_element_label);
            checkbox_label_element.appendChild(checkbox_label_element_text);
            
            var extraSettingsDiv = document.getElementById("extra_settings");
            extraSettingsDiv.insertBefore(newFormRowExtra, null);
            newFormRowExtra.insertBefore(newFormColExtra, null);
            newFormColExtra.insertBefore(newFormGroupExtra, null);
            newFormGroupExtra.appendChild(checkbox_element);
            newFormGroupExtra.appendChild(checkbox_label_element);
            }
        }
    };

// This function enables and disables the season field based on the aggregation_period field
function enableSeasonField() {
    var aggregation_period_value = document.getElementById("id_aggregation_period").value;
    if (aggregation_period_value == 'YS') {
        document.getElementById("id_season").disabled = true;
    } else {
        document.getElementById("id_season").disabled = false;
    };
};

// This function enables and disables the region field based on the region_option field
function enableRegionField() {
    region_option_value = document.getElementById("id_region_option").value;
    if (region_option_value == 'austria') {
        document.getElementById("id_region").disabled = true;
    } else {
        document.getElementById("id_region").disabled = false;
    };
};

// This function enables and disables the reference period fields based on the checkbox's state
function enableReferencePeriodFields() {
    checkbox_state = document.getElementById("id_reference_period_checkbox").checked
    if (checkbox_state) {
        document.getElementById("id_reference_period_start").disabled = false;
        document.getElementById("id_reference_period_end").disabled = false;
    } else {
        document.getElementById("id_reference_period_start").disabled = true;
        document.getElementById("id_reference_period_end").disabled = true;
    };
};

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

        console.log(colorbar_dict);
        document.getElementById("id_colorscale_colorbar_dict_extra").value = JSON.stringify(colorbar_dict);
    } else {
        alert("Step size is zero!")
    };
};

// Autocompletes region field
$(function() {
    function split( val ) {
      return val.split( /,\s*/ );
    }
    function extractLast( term ) {
      return split( term ).pop();
    }
 
    $("#id_region")
      // don't navigate away from the field on tab when selecting an item
      .on( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).autocomplete( "instance" ).menu.active ) {
          event.preventDefault();
        }
      })
      .autocomplete({
        source: function( request, response ) {
          $.getJSON( "/api/get_regions/", {
            term: extractLast( request.term),
            type: document.getElementById("id_region_option").value
          }, response );
        },
        search: function() {
          // custom minLength
          var term = extractLast( this.value );
          if ( term.length < 1 ) {
            return false;
          }
        },
        focus: function() {
          // prevent value inserted on focus
          return false;
        },
        select: function( event, ui ) {
          var terms = split( this.value );
          // remove the current input
          terms.pop();
          // add the selected item
          terms.push( ui.item.value );
          // add placeholder to get the comma-and-space at the end
          terms.push( "" );
          this.value = terms.join( ", " );
          return false;
        }
    });
});