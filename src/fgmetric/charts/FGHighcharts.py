#!/usr//bin/env python
# -*- coding: UTF-8 -*-

# FGHighcharts.py (python)
# ------------------------
import re
import sys
from datetime import timedelta, datetime

from fgmetric.util.FGUtility import FGUtility
from fgmetric.charts.FGHighchartsTemplate import FGHighchartsTemplate

class FGHighcharts:

    chart_type = ""
    html_header = ""
    html_script = ""
    html_footer = ""
    html_txt = ""
    filename = ""
    filepath = ""

    title = ""
    subtitle = ""
    tooltip = ""
    xAxis_label = []
    yAxis_title = ""
    xAxis_categories = None
    data = None
    series_name = None
    series = []
    width = 0
    height = 0

    from_date = None
    f_year = 0
    f_month = 0
    f_day = 0
    to_date = None
    t_year = 0
    t_month = 0
    t_day = 0
    days = 0

    detail_date = None
    detail_year = 0
    detail_month = 0
    detail_day = 0

    millisecond = 1000

    def __init__(self, chart_type=""):
        self.chart_type = chart_type
        self.width = 400
        self.height = 550
        self.init_options()

    def init_options(self):
        self.option_preloader = ""
        self.sort = "bykey"
        self.option_legend = { "enabled": 0 }
        #self.load_local_script_path()
        self.load_global_script_path()

    def set_type(self, name):
        self.chart_type = name

    def set_data(self, data):
        self.data = data
        if isinstance(data, (dict)):
            self.data = self.convert_dict_to_list(data)
            #self.sort_data()
            try:
                self.data = self.human_sort_data()
            except:
                try:
                    self.data = self.sort_data()
                except:
                    print sys.exc_info()
                    pass

                pass
        else:
            self.reducing_list()

    def reducing_list(self, data=None):
        data = data or self.data
            
        if not isinstance(data, (list)) or not isinstance(data[0], (list)):
            return

        res_data = sorted(data, key=lambda val:val[1], reverse=True)

        reduce_to = 20
        if len(data) <= reduce_to:
            data = res_data
            return

        count = 0
        new_data = []
        rest = ['others', 0]
        for k,v in res_data:
            if count > reduce_to:
                rest[1] += v
            else:
                new_data.append([k, v])
            count += 1
       
        rest[0] = str(count - reduce_to) + " " + rest[0]
        res_data = new_data + [rest]

        data = res_data

    def reduce_data(self, data=None):
        data = data or self.data

        if not self.chart_type in {"column", "bar"}:
            return data
           
        reduce_to = 25 
        if len(data) <= reduce_to:
            return data

        count = 0
        new_data = []
        others = ['Others', 0]
        for k,v in data:
            if count > reduce_to:
                others[1] += v
            else:
                new_data.append([k, v])
            count += 1
       
        others[0] = str(count - reduce_to) + " " + others[0]
        new_data += [others]
        return new_data

    def get_data(self, index=""):
        ''' outdated '''
        if not index == "":
            res = []
            for i in self.data:
                res.append(i[int(index)])
            return res
            
        return self.data
    def get_multi_yaxis(self):
        yaxis = []
        onleftside = 0
        guideline = 1
        colors = ['#89A54E', '#AA4643', '#4572A7']
        for record in self.series:
            color = colors.pop()
            res = { "labels": { \
                                #"formatter": "function() {return this.value +' user';}", \
                                "style": { "color": color }},\
                    "title": { "text": record["name"], \
                                "style": { "color": color } },\
                    "gridLineWidth": guideline, \
                    "opposite": onleftside }
            onleftside = 1
            guideline = 0
            yaxis.append(res)
        return yaxis

    def get_template(self, name):
        func = getattr(FGHighchartsTemplate, "get_" + name)
        return func()

    def get_template_from_file(self, filename):
        try:
            with open(filename) as f:
                lines = f.read().splitlines()
                return lines
        except:
            return []

    def convert_dict_to_list(self, data):
        dictlist = []
        for key, value in data.iteritems():
            temp = self.convert_datetime2UTC([key,value])
            dictlist.append(temp)
        return dictlist

    def sort_data(self, data=None):
        data = data or self.data
        func = getattr(self, "_sort_data_" + self.sort)
        return func(data)

    def _sort_data_bykey(self, data):
        return sorted(data, key=lambda key: key)

    def _sort_data_byvalue(self, data):
        return sorted(data, key=lambda key: key[1], reverse=True)

    def human_sort_data(self, data=None):
        data = data or self.data
        key_pat = re.compile( r"^(\D+)(\d+)$" )
        def key( item ):
            item = item[0]
            m= key_pat.match( item )
            return m.group(1), int(m.group(2))
        data.sort(key=key)
        return data
   
    def set_sort(self, by):
        self.sort = by

    def set_from_date(self, date):
        self.from_date = date
        self.f_year = date.year
        self.f_month = date.month - 1
        self.f_day = date.day

    def set_to_date(self, date):
        self.to_date = date
        self.t_year = date.year
        self.t_month = date.month - 1
        self.t_day = date.day

    def set_detail_date(self):
        self.days = (self.to_date - self.from_date).days
        days_before = self.days / 3 or 1

        self.detail_date = self.to_date - timedelta(days=days_before)
        date = self.detail_date
        self.detail_year = date.year
        self.detail_month = date.month - 1
        self.detail_day = date.day

    def set_data_name(self, data_name):
        self.series_name = data_name

    def set_series_name(self, series_name):
        self.set_data_name(series_name)

    def set_yaxis(self, title):
        self.yAxis_title = title

    def set_xaxis(self, label):
        self.xAxis_categories = label

    def set_output_path(self, path):
        try:
            FGUtility.ensure_dir(path + "/" + self.filename)
        except:
            path = "./"

        self.filepath = path

    def set_filename(self, filename):
        self.filename = filename

    def set_title(self, title):
        self.title = title

    def set_subtitle(self, subtitle):
        self.subtitle = subtitle

    def set_tooltip(self, tooltip):
        if self.chart_type == "pie":
            self.tooltip = "'<b>'+ this.point.name +'</b>: '+ this.y"
        else:
            self.tooltip = "this.x +': '+ this.y"

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = max(int(height), 150) # MINIMUM HEIGHT is 150px

    def set_series(self, data):
        try:
            for record in data:
                list_data = self.convert_dict_to_list(record["data"])
                #self.sort_data()
                try:
                    list_data = self.human_sort_data(list_data)
                except:
                    try:
                        list_data = self.sort_data(list_data)
                        list_data = self.reduce_data(list_data)
                    except:
                        print sys.exc_info()
                        pass
                    pass
                record["data"] = list_data
            self.series = data
        except:
            self.series = []

    def resize_height(self):
        new_height = self.height
        length_of_data = self.get_data_length()
        if self.chart_type in {"line-time-series", "master-detail"}:
            new_height = new_height #length_of_data * 1
        elif self.chart_type in {"column", "bar"}:
            new_height = length_of_data * 20 + 200
        elif self.chart_type in {"pie-basic-with-table"}:
            new_height += length_of_data * 10

        self.set_height(new_height)

    def convert_datetime2UTC(self, record):
        if isinstance(record[0], (datetime)):
            utc_mill = int(record[0].strftime("%s")) * self.millisecond 
            return [utc_mill, record[1]]
        else:
            return record

    def convert_UTC2date(self, date_format="%b (%Y)", data=None):
        data = data or self.data
        try:
            data = [[datetime.fromtimestamp(k / self.millisecond).strftime(date_format), v] for k,v in data]
        except:
            pass
        return data

    def convert_UTC2date_inseries(self, date_format="%b (%Y)"):
        cnt = 0
        for record in self.series:
            record["data"] = self.convert_UTC2date(date_format, record["data"])
            self.series[cnt]["data"] = record["data"]
            cnt += 1 

    def adjust_series(self):
        series_type = self.series_type
        cnt = 0
        for record in self.series:
            record["type"] = series_type
            if self.chart_type == "combo-multi-axes":
                record["yAxis"] = cnt
                cnt += 1
                # Temporary
                # primary record: column or else
                # after secondary one: line 
                series_type = "line"

        if len(self.series) == 0:
            self.series = [{ "type": series_type, \
                                "name": self.series_name, \
                                "data": self.data}]
        '''
            [{
                type: '%(series_type)s',
                name: '%(series_name)s',
                data: %(data)s
            }]
        '''

    def configure_chart_options(self):
        self.resize_height()
        self.set_chart_options()
        self.adjust_series()

    def display(self, to=None):

        try:
            self.configure_chart_options()
           
            self.html_txt = self.get_html_header() + self.get_html_script() + self.get_html_footer()
            self.html_txt = self.html_txt % vars(self)
            if to:
                to["stdout"] = self.html_txt
                return

            f = open(self.filepath + "/" + self.filename, "w")
            f.write(self.html_txt)
            f.close()
        except:
            print sys.exc_info()
            raise

    def set_chart_options(self):
        if self.chart_type == "line-time-series":
            self.set_chart_option("chart", {"renderTo": 'container', "zoomType":'x', "spacingRight": 20})
            self.set_chart_option("xAxis", {"type": 'datetime', "maxZoom": 14 * 24 * 3600000})
            self.set_chart_option("yAxis", {"title": { "text": self.yAxis_title or ""}, "min": 0.6, "startOnTick": 0, "showFirstLabel": 0}) # used 0 instead of false of javascript
            self.set_chart_option("tooltip", {"shared": 1}) # used 1 instead of true of javascript
            self.set_chart_option("plotOptions", {"area": { \
                    "fillColor": { \
                    "linearGradient": { "x1": 0, "y1": 0, "x2": 0, "y2": 1},\
                    "stops": [[0, 'rgba(0,0,0,0.5)'], \
                    #Highcharts.getOptions().colors[0]],
                    [1, 'rgba(2,0,0,0)']] }, \
                            "lineWidth": 1, \
                            "marker": { "enabled": 0, "states": { \
                                "hover": { "enabled": 1, "radius": 5} \
                                        }}, \
                                        "shadow": 0, \
                                        "states": { "hover": { "lineWidth": 1 }}}})

            self.series_type = "area"
        elif self.chart_type == "column-basic":
            self.set_chart_option("chart", {"renderTo": 'container', "type": 'column'})
            self.data = self.convert_UTC2date()
            self.set_xaxis(self.get_categories())
            self.set_chart_option("xAxis", {}) #Temporarily removed due to large length of the categories. it's not sufficieint to display #{"categories": self.xAxis_categories})
            self.set_chart_option("yAxis", {"title": { "text": self.yAxis_title or ""}})
            self.set_chart_option("tooltip", "{formatter: function() { return this.x +':<b>'+ this.y; }}")
            self.set_chart_option("plotOptions", { "column": { "cursor": 'pointer', \
                                "dataLabels": { "enabled": 1,\
                                "color": "colors[0]", \
                                "style": { "fontWeight": 'bold'}}}})
            # Temporarily removed due to large length of the categories. it's not sufficieint to display
            self.set_chart_option("plotOptions", { 'column': { 'pointPadding': 0.2, 'borderWidth': 0 } } )
            self.series_type = "column"
        elif self.chart_type == "column-stacked":
            self.set_chart_option("chart", {"renderTo": 'container', "type": 'column'})
            self.data = self.convert_UTC2date()
            self.convert_UTC2date_inseries()
            self.set_xaxis(self.get_categories())
            self.set_chart_option("xAxis", {"categories": self.xAxis_categories})
            self.set_chart_option("yAxis", { "min": 0, \
                                            "title": { "text": self.yAxis_title or ""}, \
                                            "stackLabels": { "enabled": 1, "style": {"fontWeight": 'bold', "color": 'gray' }}})
            self.set_chart_option("tooltip", {"shared":1})
            self.set_chart_option("plotOptions", { 'column': { "stacking": 'normal', "dataLabels": { "enabled": 1, "color": 'white'}}})
            self.set_chart_option("legend", {"enabled":1})
            self.series_type = "column"
        elif self.chart_type == "combo-multi-axes":
            self.set_chart_option("chart", {"renderTo": 'container', "zoomType": 'xy'})
            self.convert_UTC2date_inseries()
            self.set_xaxis(self.get_categories())
            self.set_chart_option("xAxis", {"categories": self.xAxis_categories})
            self.set_chart_option("yAxis", self.get_multi_yaxis())#{"title": { "text": self.yAxis_title or ""}})
            self.set_chart_option("tooltip", {"shared":1})#{"formatter": "function() { return this.x +':<b>'+ this.y;"})
            self.set_chart_option("plotOptions", {})
            self.series_type = "column"

        elif self.chart_type == "column-drilldown":
            self.set_chart_option("chart", {"renderTo": 'container', "type": 'column'})
            self.set_xaxis(self.get_categories())
            self.set_chart_option("xAxis", {"categories": self.xAxis_categories})
            self.set_chart_option("yAxis", {"title": { "text": self.yAxis_title or ""}})
            self.set_chart_option("tooltip", {"shared":1})#{"formatter": "function() { return this.x +':<b>'+ this.y;"})
            '''
                var point = this.point,
                s = this.x +':<b>'+ this.y +'% market share</b><br/>';
                if (point.drilldown) {
                s += 'Click to view '+ point.category +' versions';
                } else {
                s += 'Click to return to browser brands';
                }
                return s;
            '''
            self.set_chart_option("plotOptions", { "column": \
                    { "cursor": 'pointer', \
                    "dataLabels": { \
                    "enabled": 1,\
                    "color": "colors[0]", \
                    "style": {\
                        "fontWeight": 'bold'\
                        }\
                        }#"formatter": "function() { return this.y;}" } \
                    }})

            self.series_type = "column"
        elif self.chart_type == "pie-basic":
            chart_name = "pie"
            self.height = 440
            self.set_chart_option("chart", {"renderTo": 'container'})
            self.set_chart_option("xAxis", {})
            self.set_chart_option("yAxis", {})
            self.set_chart_option("tooltip", {"pointFormat":"{series.name}: <b>{point.percentage}</b>", "percentageDecimals":1})
            '''
            self.set_chart_option("plotOptions", { chart_name: \
                    { "allowPointSelect":1, \
                    "cursor": 'pointer', \
                    "dataLabels": { \
                    "enabled": 1,\
                    "color": "#000000", \
                    "connectorColor": "#000000", \
                        }#"formatter": "function() { return this.y;}" } \
                    }})
            '''
            self.set_chart_option("plotOptions", "{'pie': { 'size': 180, 'cursor': 'pointer', 'dataLabels': {'color': '#000000', 'connectorColor': '#000000', 'enabled': 1,formatter: function() {\
                    var strLength = 25; var trimmedString = this.point.name.length > strLength ? this.point.name.substring(0, strLength - 3) + ' ...' : this.point.name.substring(0, strLength);\
                    return '<b>'+ trimmedString +'</b>: '+ Math.round(this.percentage*100)/100 +' %';\
                    }}, 'allowPointSelect': 1}}")
            self.series_type = chart_name
        elif self.chart_type == "pie-basic-with-table":
            chart_name = "pie"
            spacing = self.get_data_length() * 10 + 250
            self.set_chart_option("chart", "{ renderTo: 'container', events: { load: Highcharts.drawTable }, marginBottom: " + str(spacing) + " }")
            self.set_chart_option("xAxis", {})
            self.set_chart_option("yAxis", {})
            self.set_chart_option("tooltip", {"pointFormat":"{series.name}: <b>{point.percentage}</b>", "percentageDecimals":1})
            self.set_chart_option("plotOptions", "{'pie': { 'size': 180, 'cursor': 'pointer', 'dataLabels': {'color': '#000000', 'connectorColor': '#000000', 'enabled': 1,formatter: function() {\
                    var strLength = 25; var trimmedString = this.point.name.length > strLength ? this.point.name.substring(0, strLength - 3) + ' ...' : this.point.name.substring(0, strLength);\
                    return '<b>'+ trimmedString +'</b>: '+ Math.round(this.percentage*100)/100 +' %';\
                    }}, 'allowPointSelect': 1}}")
            self.series_type = chart_name
            template = self.get_template("datatable2pie")
            self.set_chart_option("preloader", template)
        else:
            #default options
            self.set_chart_option("chart", {"renderTo": 'container', "type": self.chart_type})
            if not self.xAxis_categories:
                self.set_xaxis(self.get_categories())
            self.set_chart_option("xAxis", {"categories": self.xAxis_categories})
            self.set_chart_option("yAxis", {"min": 0, "title": { "text": self.yAxis_title or ""}})
            self.set_chart_option("tooltip", {"formatter": "function() { return ''+ " + self.tooltip + "; }" })
            self.set_chart_option("plotOptions", { self.chart_type: { "dataLabels":{"enabled":1}, "pointPadding": 0.2, "borderWidth": 0 } })
            self.series_type = self.chart_type

    def set_chart_option(self, key, val):
        setattr(self, "option_" + str(key), val)
        #option = getattr(self, "option_" + str(key))
      
    def get_categories(self):
        try:
            return list(zip(*self.series[0]["data"])[0])
        except:
            return list(zip(*self.data)[0])

    def get_data_length(self):
        try:
            return len(self.series[0]["data"])
        except:
            return len(self.data)

    def load_script_path(self, name):
        func = getattr(self, "load_" + str(name) + "_script_path")
        func()

    def load_local_script_path(self):
        self.set_chart_option("script_path1", "../../../../../../_static/js")
        self.set_chart_option("script_path2", "../../../../../../_static/js")

    def load_global_script_path(self):
        self.set_chart_option("script_path1", "http://code.jquery.com")
        self.set_chart_option("script_path2", "http://code.highcharts.com")

    def get_html_header(self):
        self.html_header = '''<!DOCTYPE html>
        <html>
        <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <meta http-equiv="cache-control" content="max-age=0" />
        <meta http-equiv="cache-control" content="no-cache" />
        <meta http-equiv="expires" content="0" />
        <meta http-equiv="expires" content="Tue, 01 Jan 1980 1:00:00 GMT" />
        <meta http-equiv="pragma" content="no-cache" />
        <script type='text/javascript' src='%(option_script_path1)s/jquery-1.7.2.min.js'></script>'''
        return self.html_header

    def get_html_script(self):
        self.html_script = '''
        <script type='text/javascript'>
        //<![CDATA[ 
            $(function () {
                %(option_preloader)s
                var chart;
                $(document).ready(function() {
                var colors = Highcharts.getOptions().colors,
                    chart = new Highcharts.Chart({
                        chart: %(option_chart)s,
                        title: {
                            text: '%(title)s'
                            },
                        subtitle: {
                        text: '%(subtitle)s'
                            },
                        xAxis: %(option_xAxis)s,
                        yAxis: %(option_yAxis)s,
                        legend: %(option_legend)s,
                        tooltip: %(option_tooltip)s,
                        plotOptions: %(option_plotOptions)s, 
                        series: %(series)s
                        });
                    });
            });
        //]]>  
        </script>'''
        # Legend removed for some reason. 01/09/2013
        '''
                        legend: {
                            layout: 'vertical',
                            backgroundColor: '#FFFFFF',
                            align: 'right',
                            verticalAlign: 'top',
                            x: -100,
                            y: 70,
                            floating: true,
                            shadow: true
                            },
        '''
 
        if self.chart_type == "master-detail":
            self.html_script = '''<script type='text/javascript'>
                //<![CDATA[ 
                $(function () {
                var data = %(data)s ;
                
                var masterChart,
                    detailChart;
                
                $(document).ready(function() {
                
                    // create the master chart
                    function createMaster() {
                        masterChart = new Highcharts.Chart({
                            chart: {
                                renderTo: 'master-container',
                                reflow: false,
                                borderWidth: 0,
                                backgroundColor: null,
                                marginLeft: 50,
                                marginRight: 20,
                                zoomType: 'x',
                                events: {
                
                                    // listen to the selection event on the master chart to update the
                                    // extremes of the detail chart
                                    selection: function(event) {
                                        var extremesObject = event.xAxis[0],
                                            min = extremesObject.min,
                                            max = extremesObject.max,
                                            detailData = [],
                                            xAxis = this.xAxis[0];
                
                                        // reverse engineer the last part of the data
                                        jQuery.each(this.series[0].data, function(i, point) {
                                            if (point.x > min && point.x < max) {
                                                detailData.push({
                                                    x: point.x,
                                                    y: point.y
                                                });
                                            }
                                        });
                
                                        // move the plot bands to reflect the new detail span
                                        xAxis.removePlotBand('mask-before');
                                        xAxis.addPlotBand({
                                            id: 'mask-before',
                                            from: Date.UTC(%(f_year)s, %(f_month)s, %(f_day)s),
                                            to: min,
                                            color: 'rgba(0, 0, 0, 0.2)'
                                        });
                
                                        xAxis.removePlotBand('mask-after');
                                        xAxis.addPlotBand({
                                            id: 'mask-after',
                                            from: max,
                                            to: Date.UTC(%(t_year)s, %(t_month)s, %(t_day)s),
                                            color: 'rgba(0, 0, 0, 0.2)'
                                        });
                
                
                                        detailChart.series[0].setData(detailData);
                
                                        return false;
                                    }
                                }
                            },
                            title: {
                                text: null
                            },
                            xAxis: {
                                type: 'datetime',
                                showLastTickLabel: true,
                                maxZoom: 14 * 24 * 3600000, // fourteen days
                                plotBands: [{
                                    id: 'mask-before',
                                    from: Date.UTC(%(f_year)s, %(f_month)s, %(f_day)s),
                                    to: Date.UTC(%(detail_year)s, %(detail_month)s, %(detail_day)s),
                                    color: 'rgba(0, 0, 0, 0.2)'
                                }],
                                title: {
                                    text: null
                                }
                            },
                            yAxis: {
                                gridLineWidth: 0,
                                labels: {
                                    enabled: false
                                },
                                title: {
                                    text: null
                                },
                                min: 0.6,
                                showFirstLabel: false
                            },
                            tooltip: {
                                formatter: function() {
                                    return false;
                                }
                            },
                            legend: {
                                enabled: false
                            },
                            credits: {
                                enabled: false
                            },
                            plotOptions: {
                                series: {
                                    fillColor: {
                                        linearGradient: [0, 0, 0, 70],
                                        stops: [
                                            [0, '#4572A7'],
                                            [1, 'rgba(0,0,0,0)']
                                        ]
                                    },
                                    lineWidth: 1,
                                    marker: {
                                        enabled: false
                                    },
                                    shadow: false,
                                    states: {
                                        hover: {
                                            lineWidth: 1
                                        }
                                    },
                                    enableMouseTracking: false
                                }
                            },
                
                            series: [{
                                type: 'area',
                                name: '%(series_name)s',
                                pointInterval: 24 * 3600 * 1000,
                                pointStart: Date.UTC(%(f_year)s, %(f_month)s, %(f_day)s),
                                data: data
                            }],
                
                            exporting: {
                                enabled: false
                            }
                
                        }, function(masterChart) {
                            createDetail(masterChart)
                        });
                    }
                
                    // create the detail chart
                    function createDetail(masterChart) {
                
                        // prepare the detail chart
                        var detailData = [],
                            detailStart = Date.UTC(%(detail_year)s, %(detail_month)s, %(detail_day)s);
                
                        jQuery.each(masterChart.series[0].data, function(i, point) {
                            if (point.x >= detailStart) {
                                detailData.push(point.y);
                            }
                        });
                
                        // create a detail chart referenced by a global variable
                        detailChart = new Highcharts.Chart({
                            chart: {
                                marginBottom: 120,
                                renderTo: 'detail-container',
                                reflow: false,
                                marginLeft: 50,
                                marginRight: 20,
                                style: {
                                    position: 'absolute'
                                }
                            },
                            credits: {
                                enabled: false
                            },
                            title: {
                                text: '%(title)s'
                            },
                            subtitle: {
                                text: '%(subtitle)s'
                            },
                            xAxis: {
                                type: 'datetime'
                            },
                            yAxis: {
                                title: {
                                    text: null
                                },
                                maxZoom: 0.1
                            },
                            tooltip: {
                                formatter: function() {
                                    var point = this.points[0];
                                    return '<b>'+ point.series.name +'</b><br/>'+
                                        Highcharts.dateFormat('%%A %%B %%e %%Y', this.x) + ':<br/>'+
                                        ' ' + Highcharts.numberFormat(point.y, 0) + ' ';
                                },
                                shared: true
                            },
                            legend: {
                                enabled: false
                            },
                            plotOptions: {
                                series: {
                                    marker: {
                                        enabled: false,
                                        states: {
                                            hover: {
                                                enabled: true,
                                                radius: 3
                                            }
                                        }
                                    }
                                }
                            },
                            series: [{
                                name: '%(series_name)s',
                                pointStart: detailStart,
                                pointInterval: 24 * 3600 * 1000,
                                data: detailData
                            }],
                
                            exporting: {
                                enabled: false
                            }
                
                        });
                    }
                
                    // make the container smaller and add a second container for the master chart
                    var $container = $('#container')
                        .css('position', 'relative');
                
                    var $detailContainer = $('<div id="detail-container">')
                        .appendTo($container);
                
                    var $masterContainer = $('<div id="master-container">')
                        .css({ position: 'absolute', top: 300, height: 80, width: '100%%' })
                        .appendTo($container);
                
                    // create master and in its callback, create the detail chart
                    createMaster();
                });
                
            });
                    //]]>  
                    </script>'''

        return self.html_script

    def get_html_footer(self):
        self.html_footer = '''
        </head>
        <body>
        <script src="%(option_script_path2)s/highcharts.js"></script>
        <script src="%(option_script_path2)s/modules/exporting.js"></script>
        <div id="container" style="width: 100%%; height: %(height)dpx; margin: 0 auto"></div>
        </body>
        </html>
        ''' 
        return self.html_footer
