from fgmetric.FGPygooglechart import FGPyGoogleChart
from fgmetric.FGHighcharts import FGHighcharts
from fgmetric.FGUtility import FGUtility

class FGCharts:

    def __init__(self):
        self.chart = None
        self.chart_api = None
        self.type = None
        self.data = None
        self.data_name = "all"
        self.xaxis = None
        self.yaxis = None
        self.output_path = "./"#None
        self.output_type = "html"
        self.title = "FG Charts"#None
        self.subtitle = ""#None
        self.filename = FGUtility.timeStamped("chart") + "." + self.output_type#None

    def set_chart_api(self, name="highcharts"):
        self.chart_api = name

    def set_type(self, name):
        self.type = name

    def set_output_path(self, name):
        self.output_path = name

    def set_output_type(self, name):
        self.output_type = name

    def set_xaxis(self, value):
        self.xaxis = value

    def set_yaxis(self, value):
        self.yaxis = value

    def set_data(self, data):
        self.data = data

    def set_title(self, name):
        self.title = name

    def set_subtitle(self, name):
        self.subtitle = name
 
    def clear_data(self):
        self.xaxis = None
        self.yaxis = None
        self.data = None

    def set_data_beta(self, data, *keynames):
        if not keynames:
            return data

        for keyname in keynames:
            if not keyname:
                continue
            data = data[keyname]

        try:
            if type(data) == type({}):
                self.set_data(data)
        except:
            pass

    def set_datafromdict(self, data, keyname=None):
        '''
         Example of data: {'nimbus': {'count': 77}, 'eucalyptus': {'count': 119}}
         The template is like: group1: {name of y axis: value, ...}, ...
         possible ways that I can think of are ...
         1. { metric: value }
         2. { group1: { metric: value}, ...
         3. { group1: { metric1: value, ... }, ...
        ''' 
        xaxis = []
        yaxis = []
        series = {}
        
        try:
            if type(data) == type({}):
                xaxis = data.keys()
                records = data.values()
                yaxis = records[0].keys()
                for name in yaxis: # count
                    for record in records: # {'count': 77}, {'count':119}
                        if not name in series:
                            series[name] = []
                        series[name].append(record[name])

                self.set_xaxis(xaxis)
                #self.chart.set_series(seriese
                #self.chart.set_data_name(series.keys())
                self.set_data(",".join(str(x) for x in series.values()))
        except:
            pass

    def _create_chart(self):
        try:
            # inherit object variables?
            if self.chart_api == "highcharts":
                self.chart = FGHighcharts()
            elif self.chart_api == "googlechart":
                self.chart = FGPyGoogleChart()
            self.chart.set_type(self.type)
            self.chart.set_data(self.data)
            # highcharts
            self.chart.set_data_name(self.data_name)
            self.chart.set_subtitle(self.subtitle)
            self.chart.set_xaxis(self.xaxis)
            self.chart.set_yaxis(self.yaxis)
            self.chart.set_output_path(self.output_path)
            self.chart.set_title(self.title)
            self.chart.set_filename(self.filename)
            self.chart.set_tooltip("")
        except:
            pass

    def display(self):

        self._create_chart() # default
        self.chart.display()
