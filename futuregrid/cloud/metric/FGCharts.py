from futuregrid.cloud.metric.FGPygooglechart import PyGoogleChart
from futuregrid.cloud.metric.FGHighcharts import Highcharts

class Charts:

    def __init__(self):
        self.chart = None
        self.chart_name = None
        self.type = None
        self.data = None
        self.data_name = None
        self.xaxis = None
        self.yaxis = None
        self.output_path = None
        self.output_type = "html"
        self.title = None
        self.filename = None

    def set_chart(self, name):
        self.chart_name = name
        if name == "highcharts":
            self.chart = Highcharts()
        elif name == "googlechart":
            self.chart = PyGoogleChart()

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

    def display(self):
        self.chart.display()
