from fgmetric.FGPygooglechart import FGPyGoogleChart
from fgmetric.FGHighcharts import FGHighcharts

class FGCharts:

    def __init__(self):
        self.chart = None
        self.chart_name = None
        self.type = None
        self.data = None
        self.data_name = "all"
        self.xaxis = None
        self.yaxis = None
        self.output_path = None
        self.output_type = "html"
        self.title = None
        self.subtitle = None
        self.filename = None

    def set_chart(self, name="highcharts"):
        self.chart_name = name

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
 
    def clear_data(self):
        self.xaxis = None
        self.yaxis = None
        self.data = None

    # How to create heritage of variables to a child object?

    def _create_chart(self):
        try:
            if self.chart_name == "highcharts":
                self.chart = FGHighcharts()
            elif self.chart_name == "googlechart":
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
