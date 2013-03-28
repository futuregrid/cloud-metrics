from fgmetric.charts.FGPygooglechart import FGPyGoogleChart
from fgmetric.charts.FGHighcharts import FGHighcharts
from fgmetric.util.FGUtility import FGUtility
import sys

class FGCharts:

    def __init__(self):
        self.chart = None
        self.chart_api = None
        self.type = None
        self.data = None
        self.data_name = "all"
        self.series = []
        self.data_beta = { "type":None, "name":None, "data":None } 
        self.xaxis = None
        self.yaxis = None
        self.output_path = "./"#None
        self.output_type = "html"
        self.title = "FG Charts"#None
        self.subtitle = ""#None
        self.filename = FGUtility.timeStamped("chart") + "." + self.output_type#None
        self.script_path = "global"#"local"

        self.sort = "bykey"

    def set_chart_api(self, name="highcharts"):
        self.chart_api = name

    def set_type(self, name):
        self.type = name
        # for those charts, we use sorting by value
        if name[:3] in { "pie", "bar" }:
            self.set_sort("byvalue")

    def set_sort(self, by):
        self.sort = by

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

    def set_title_beta(self, metric, period, groupby):
        title = metric
        plus = ""
        if period:
            plus = " (" + str(period) + ")"
        if groupby:
            plus = " by " + str(groupby) + plus
        self.title = title + plus

    def set_subtitle(self, name):
        self.subtitle = name

    def set_filename(self, name):
        self.filename = name
 
    def clear_data(self):
        self.xaxis = None
        self.yaxis = None
        self.data = None

    def set_series(self, data):
        self.series = data

    def set_data_beta(self, data, *keynames):

        try:
            for keyname in keynames:
                try:
                    data = data[keyname]
                except:
                    continue
        except:
            pass

        try:
            self.set_data(data)
        except:
            pass

    def set_data_beta2(self, key, val, *keynames):
        '''
         Example of data: {'nimbus': {'count': {'Total':77}}, 'eucalyptus': {'count': {'Total':119}}}
         The template is like: group1: {name of y axis: value, ...}, ...
         possible ways that I can think of are ...
         1. { metric: { type : value } }
         2. { group1: { metric: { type: value } }, ...
         3. { group1: { metric1: { type: value }, ... }, ...
        ''' 
        
        try:
            for keyname in keynames:
                try:
                    val = val[keyname]
                except:
                    continue
        except:
            pass

        # doesnt cover val is dict which is not integer.
        # if we choose period monthly, or daily, val shoulde be like {datetime.datetime... : integer value, ...}
        res = [key,val]
        try:
            self.data.append(res)
        except:
            self.set_data([])
            self.data.append(res)

        '''
            records = dataes() # {'count':...}
            yaxis = records[0].keys() # 'count'
            for name in yaxis: # count
                for record in records: # {'count': {'Total':77}}, {'count':{'Total':119}}
                    if not name in series:
                        series[name] = []
                    if keyname:
                        series[name].append(record[name][keyname])
                    else:
                        series[name].append(record[name])

            self.set_xaxis(xaxis)
            #self.chart.set_series(seriese
            #self.chart.set_data_name(series.keys())
            self.set_data(",".join(str(x) for x in series.values()))
        except:
            pass
        '''

    def load_script_path(self, name):
        self.script_path = name

    def _create_chart(self):
        try:
            # inherit object variables?
            if self.chart_api == "highcharts":
                self.chart = FGHighcharts()
            elif self.chart_api == "googlechart":
                self.chart = FGPyGoogleChart()
            self.chart.set_type(self.type)
            self.chart.set_sort(self.sort)
            self.chart.set_data(self.data)
            # highcharts
            self.chart.set_data_name(self.data_name)
            self.chart.set_series(self.series)
            self.chart.set_subtitle(self.subtitle)
            self.chart.set_xaxis(self.xaxis)
            self.chart.set_yaxis(self.yaxis)
            self.chart.set_output_path(self.output_path)
            self.chart.set_title(self.title)
            self.chart.set_filename(self.filename)
            self.chart.set_tooltip("")
            self.chart.load_script_path(self.script_path)
        except:
            print sys.exc_info()
            pass

    def display(self, opts=None):

        self._create_chart() # default
        self.chart.display(opts)
