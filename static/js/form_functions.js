window.onload = function () {
    productTypeSettings();

    document.getElementById("id_region_option").onchange = enableRegionField;
    document.getElementById("id_aggregation_period").onchange = enableSeasonField;
    document.getElementById("id_product_type").onchange = productTypeSettings;
    document.getElementById("collapse_button").onclick = collapseEvents;
    document.getElementById("colorbar_generate_button").onclick = reDrawColorBarButtonClicked;
    document.getElementById("id_reference_period_checkbox").onchange = enableReferencePeriodFields;
    document.getElementById("id_colorscale_name_extra").onchange = colorBarChanged;
    document.getElementById("formfill_button").onclick = fillFormWithPOST;
};

function reDrawColorBarButtonClicked() {
    // make colorbar innerHTML empty
    makeColorBarDivInnerHTMLEmpy();
    // redraw colorbar div
    createColorScaleDiv(create_html_colordict(redraw = true));
    // update colorbar dict
    updateColorBarDict(createColorBarDict());
};

function colorBarChanged() {
    // get colorbar features
    var colorbar_features = getColorBarFeatures();
    // fill in colorbar related fields
    setColorBarFields(colorbar_features);
    // make colorbar innerHTML empty
    makeColorBarDivInnerHTMLEmpy();
    // redraw colorbar div
    createColorScaleDiv(create_html_colordict(redraw = false));
    // update colorbar dict
    updateColorBarDict(createColorBarDict());
};

function collapseColorBarChanges() {
    // check if colorbar dict is empty, if yes
    if (document.getElementById("id_colorscale_colorbar_dict_extra").value == '') {
        // colorBarChanged
        colorBarChanged();
    };
};

// ############# colorbar related functions #################################

function setColorBarFields(cbar_fields_dict) {
    document.getElementById("id_colorscale_minval_extra").value = cbar_fields_dict['minval'];
    document.getElementById("id_colorscale_step_size_extra").value = cbar_fields_dict['step'];
    document.getElementById("id_colorscale_reverse_extra").value = cbar_fields_dict['reverse'];
};

function getColorBarFeatures(colorscale = "None") {
    var colorscales = JSON.parse(getStaticFile('products/static/colorscales.json'));
    if (colorscale == "None") {
        var selected_colorscale = document.getElementById("id_colorscale_name_extra").value;
    } else {
        var selected_colorscale = colorscale;
    };
    return colorscales[selected_colorscale];
};

function collectColorBarFields() {
    var dict = {
        colorscale: document.getElementById("id_colorscale_name_extra").value,
        minval: parseFloat(document.getElementById("id_colorscale_minval_extra").value),
        step: parseFloat(document.getElementById("id_colorscale_step_size_extra").value),
        reverse: document.getElementById("id_colorscale_reverse_extra").checked,
    };
    return dict
};

function makeColorBarDivInnerHTMLEmpy() {
    document.getElementById("colorbar_colors").innerHTML = "";
};

function updateColorBarDict(cbar_dict) {
    document.getElementById("id_colorscale_colorbar_dict_extra").value = JSON.stringify(cbar_dict);
};

// This function creates a dictionary for the html POST request
function createColorBarDict() {
    var field_values = collectColorBarFields();
    var colors = JSON.parse(getStaticFile('products/static/colors.json'));
    color_count = colors[field_values['colorscale']].length;

    if (field_values['step'] != 0.0) {
        if (field_values['step'] > 0) {
            var new_min = field_values['minval'];
            var new_max = new_min + ((color_count-1) * field_values['step']);
        } else {
            var new_min = field_values['minval'] + ((color_count-1) * field_values['step']);
            var new_max = field_values['minval'];
        };

        colorbar_dict = {
            'color_scale': field_values['colorscale'],
            'minval': parseFloat(new_min.toFixed(1)),
            'maxval': parseFloat(new_max.toFixed(1)),
            'step_size': field_values['step'],
            'bins': 'None',
            'color_count': color_count,
            'reverse': field_values['reverse']
        };

        return colorbar_dict;
    } else {
        alert("Step size is zero!")
    };
};

function create_html_colordict(redraw = false) {
    var colorscales = JSON.parse(getStaticFile('products/static/colorscales.json'));
    var colors = JSON.parse(getStaticFile('products/static/colors.json'));

    var colorscale_fields = collectColorBarFields();
    var selected_colorscale_features = colorscales[colorscale_fields['colorscale']];
    var selected_colors = colors[colorscale_fields['colorscale']];

    var colorbar_reversed = false;
    if (redraw == true) {
        if (colorscale_fields['reverse'] == true) {
            var selected_colors = selected_colors.reverse();
            colorbar_reversed = true;
        };
        var minval = colorscale_fields['minval'];
        var step = colorscale_fields['step'];
    } else {
        var minval = selected_colorscale_features["minval"];
        var step = selected_colorscale_features["step"];
        document.getElementById("id_colorscale_minval_extra").value = minval;
        document.getElementById("id_colorscale_step_size_extra").value = step;
    };
    value_array = []
    for (var i = 0; i < selected_colors.length; i++) {
        val = (minval + (i * step)).toFixed(1);
        value_array.push(val);
    };

    var html_colordict = {
        colors: colors[colorscale_fields['colorscale']],
        values: value_array,
        step: step,
        reversed: colorbar_reversed,
        unit: selected_colorscale_features["unit"]
    };
    return html_colordict;
};

function createColorScaleDiv(colordict) {
    function checkDigit(val) {
        return parseFloat(val) % 1 != 0;
    };

    function replaceZero(x) {
        return x.replace(/\.0/, "")
    };

    if (colordict['values'].some(checkDigit) == false) {
        var values_string = colordict['values'].map(replaceZero);
    } else {
        var values_string = colordict['values'];
    };

    var numeric_values = colordict['values'].map(Number);
    var colorBarDiv = document.getElementById("colorbar_colors");
    var newTable = document.createElement("TABLE");
    newTable.classList.add("table");
    newTable.classList.add("colorbar_colors");
    colorBarDiv.insertBefore(newTable, null)
    var tableRowColor = newTable.insertRow(0);
    var colors = colordict['colors'];
    var colorCount = colors.length;
    var td_width = (1 / colorCount).toString().concat('%')

    for (i = 0; i < colorCount; i++) {
        var newTableDataColor = tableRowColor.insertCell(i);
        newTableDataColor.style.backgroundColor = colors[i];
        newTableDataColor.style.width = td_width;
        newTableDataColor.style.height = '70px';
        newTableDataColor.style.padding = '0';
        newTableDataColor.title = values_string[i]
            + ' — ' + values_string[i + 1];
    };

    var colorBarDivInfo = document.getElementById("colorbar_values");
    colorBarDivInfo.innerHTML = 'Actual min: ' + Math.min.apply(Math, numeric_values)
        + ', max: ' + Math.max.apply(Math, numeric_values) + ', step: ' + colordict['step']
        + ', reversed: ' + colordict['reversed']
    colorBarDivInfo.style.color = 'white';

};

// ############# end of colorbar related functions ##########################


// This function enlarges or shrinks the paragraph based on it's actual size, connected to a button
function collapseEvents() {
    var product_widgets = getProductFeatures(field_name = 'widgets');
    var parsed_product_widgets = JSON.parse(product_widgets);
    var widget_keys = Object.keys(parsed_product_widgets['widgets']);
    var cscale = widget_keys.includes('colorscale');
    var number_of_widgets = widget_keys.length;

    // here we add the extra buttons
    if (document.getElementById("collapse_button").getAttribute("aria-expanded") == "false") {
        emptyFieldSize(number_of_widgets, colorscale = cscale);
        collapseColorBarChanges();
        enableDisableCheckboxes(product_widgets);
    } else {
        emptyFieldSize(0, colorscale=false);
    };
};

function emptyFieldSize(n, colorscale) {
    // here we add some more space below extra settings
    var empty_field = document.getElementById("empty-black-space");
    var r = (n > 0) ? 1 : 0;
    var size = (n - r) * 40;
    if (colorscale == true) {
        size = size + 300;
    }
    var size_str = size.toString() + "px"
    empty_field.style.height = size_str;
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
        parameter2_field.disabled = false;
    } else {
        parameter2_field.style.visibility = "hidden";
        parameter2_field.disabled = true;
    };

    // set period boundaries
    var dataset = parsed_productFeatures['dataset'];
    var ps = document.getElementById("id_period_start");
    var pe = document.getElementById("id_period_end");
    if (dataset == 'oeks') {
        ps.value = "2021";
        pe.value = "2050";
        ps.min = "1971";
        ps.max = "2099";
        pe.min = "1972";
        pe.max = "2100";
    } else if (dataset == 'spartacus') {
        ps.value = "1961";
        pe.value = "1990";
        ps.min = "1961";
        ps.max = "2017";
        pe.min = "1962";
        pe.max = "2018";
    } else if (dataset == 'spartacus_oeks') {
        ps.value = "1971";
        pe.value = "2100";
        ps.min = "1971";
        ps.max = "2099";
        pe.min = "1972";
        pe.max = "2100";
    };

    // lock reference perid checkbox
    var product_must_have_reference_period = parsed_productFeatures['must_have_reference_period'];
    var ref_per_checkbox = document.getElementById("id_reference_period_checkbox");
    if (product_must_have_reference_period == true) {
        ref_per_checkbox.required = true;
    } else {
        ref_per_checkbox.required = false;
    }

    // enable/disable output types
    select_output_types(parsed_productFeatures);

    var product_widgets = getProductFeatures(field_name = 'widgets');
    var product_widgets_str = JSON.stringify(product_widgets);
    enableDisableCheckboxes(product_widgets);

    // show/hide color related fields
    if (product_widgets_str.includes("colorscale") == false) {
        document.getElementById("color_related_fields").style.display = "none";
    } else {
        document.getElementById("color_related_fields").style.display = "block";
    };
};

// ## form field functions ##

function enableDisableCheckboxes(pc) {
    var product_checkboxes = JSON.parse(pc)['widgets'];
    var product_widget_keys = Object.keys(product_checkboxes);
    var all_widgets = JSON.parse(getModelObjects('widget'))['objects'];
    var all_keys = Object.keys(all_widgets);
    var key_number = all_keys.length;
    for (var i = 0; i < key_number; i++) {
        var elem = all_keys[i];
        var extended_widget_name = "id_".concat(elem).concat("_extra");
        if (elem != 'colorscale') {
            if (product_widget_keys.includes(elem) && all_widgets[elem]['enabled'] == true) {
                document.getElementById(extended_widget_name).style.display = "block";
            } else {
                document.getElementById(extended_widget_name).style.display = "none";
            };
        };
        
    };
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
    document.getElementById("id_region").value = "";
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

function select_output_types(product_features) {
    var output_type_field = document.getElementById("id_output_type");
    var output_count = output_type_field.options.length;
    var product_type_outputs = product_features['output_types'];
    var first = true;
    for (i = 0; i < output_count; i++) {
        var mod_i = i.toString().concat(',');
        if (product_type_outputs.includes(mod_i) == true) {
            output_type_field.options[i].disabled = false;
            if (first == true) {
                output_type_field.selectedIndex = i.toString();
                first = false;
            };
        } else {
            output_type_field.options[i].disabled = true;
        };
    };
};

// ## end of form field functions ##

// ## AJAX requests ## //

function getStaticFile(url, callback) {
    var file_contents = $.ajax({
        url: "/api/get_static_file/",
        type: "GET",
        async: false,
        dataType: 'json',
        data: {
            file: url
        }
    });
    return file_contents.responseText;
};

function getProductFeatures(field_name, set_async = false, callback) {
    var widgets_call_result = $.ajax({
        url: "/api/get_product_features/",
        type: "GET",
        async: set_async,
        dataType: 'json',
        data: {
            product_name: document.getElementById("id_product_type").value,
            field: field_name
        }
    });
    return widgets_call_result.responseText;
};

function getModelObjects(model, callback) {
    var widgets_call_result = $.ajax({
        url: "/api/get_model_objects/",
        type: "GET",
        async: false,
        dataType: 'json',
        data: {
            model: model
        }
    });
    return widgets_call_result.responseText;
};

// Autocompletes region field
$(function () {
    function split(val) {
        return val.split(/,\s*/);
    }
    function extractLast(term) {
        return split(term).pop();
    }

    $("#id_region")
        // don't navigate away from the field on tab when selecting an item
        .on("keydown", function (event) {
            if (event.keyCode === $.ui.keyCode.TAB &&
                $(this).autocomplete("instance").menu.active) {
                event.preventDefault();
            }
        })
        .autocomplete({
            source: function (request, response) {
                $.getJSON("/api/get_regions/", {
                    term: extractLast(request.term),
                    type: document.getElementById("id_region_option").value
                }, response);
            },
            search: function () {
                // custom minLength
                var term = extractLast(this.value);
                if (term.length < 2) {
                    return false;
                }
            },
            focus: function () {
                // prevent value inserted on focus
                return false;
            },
            select: function (event, ui) {
                var terms = split(this.value);
                // remove the current input
                terms.pop();
                // add the selected item
                terms.push(ui.item.value);
                // add placeholder to get the comma-and-space at the end
                terms.push("");
                this.value = terms.join(", ");
                return false;
            }
        });
});

// ## end of AJAX requests ## //

// function to refill form

function fillFormWithPOST() {
    testDict = {
        "id_product_type": "barcode_spartacus",
        "id_scenario": "rcp26",
        "id_parameter": "cdd",
        "id_parameter2": "cdd",
        "id_aggregation_period": "YS",
        "id_season": "DJF",
        "id_region_option": "austria",
        "id_region": "",
        "id_period_start": "2021",
        "id_period_end": "2050",
        "id_reference_period_checkbox": "on",
        "id_reference_period_start": "1971",
        "id_reference_period_end": "2000",
        "id_lower_height_filter": "0",
        "id_upper_height_filter": "0",
        "id_output_type": "pdf",
        "id_output_path": "",
        "id_colorscale_colorbar_dict_extra": '{"color_scale":"alfa","minval":-19.5,"maxval":34.5,"step_size":1,"bins":"None","color_count":55,"reverse":false}',
        "id_colorscale_name_extra": "alfa",
        "id_colorscale_minval_extra": "-19.5",
        "id_colorscale_step_size_extra": "1",
        "id_colorscale_reverse_extra": "False",
        "id_rivers_extra": "False",
        "id_municipality_borders_extra": "False",
        "id_state_borders_extra": "on",
        "id_country_borders_extra": "False",
        "id_hillshade_extra": "False",
        "id_linediagram_grid_extra": "False",
        "id_smooth_extra": "False",
        "id_infobox_extra": "False",
        "id_boxplot_extra": "False",
        "id_title_extra": "False",
        "id_secondary_y_axis_extra": "False"
    };

    var testDict_keys = Object.keys(testDict);
    var i;
    for (i = 0; i<testDict_keys.length;i++) {
        document.getElementById(testDict_keys[i]).value = testDict[testDict_keys[i]];
    };

}
