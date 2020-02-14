

class ProductRequest:
    def __init__(self, product_type, parameter, aggregation_period, season, scenario,
        region_option, region, period, reference_period, lower_height_filter,
        upper_height_filter, visual_settings, output_path, output_type):
        '''Initialize class'''
        self.product_type = product_type
        self.parameter = parameter
        self.aggregation_period = aggregation_period
        self.season = season
        self.scenario = scenario
        self.region_option = region_option
        self.region = region
        self.period = period
        self.reference_period = reference_period
        self.lower_height_filter = lower_height_filter
        self.upper_height_filter = upper_height_filter
        self.visual_settings = visual_settings
        self.output_path = output_path
        self.output_type = output_type

        self.model_statistics = 'mean'

        self.dataset = 'oeks' #product_catalog[self.product_type]['dataset']
        self.outname = 'test_name' #self.product_output_name_generator()
