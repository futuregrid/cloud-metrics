import datetime
from futuregrid.cloud.metric.FGUtility import Utility
class Results:
    ''' This generates reports from (start_date) to (t_end_date) in (name) directory as restructuredText files.
        In case that you want to change period of reports, simple change (start_date) and (t_end_date) in this file.
        And run sphinx-build to generate html files. '''

    name = "results"
    docs_ext = ".rst"
    start_date = datetime.date(2011, 10, 31)
    start_date_for_weekly = start_date
    t_end_date = datetime.date(2012, 06, 11)
    end_date = start_date + datetime.timedelta(days=6)
    week = datetime.timedelta(weeks=1)
    index_txt = None
    index_filename = name + docs_ext

    docs_path = name + "/"
    indent = "\t"
    newline = "\n"

    def generate_index_and_contents(self):

        index_txt = ""

        while (1):
            if self.start_date > self.t_end_date:
                break
            
            self.end_date = self.start_date + datetime.timedelta(days=6)
            if (self.start_date_for_weekly + (10 * self.week)) == self.start_date:
                self.start_date_for_weekly = self.start_date_for_weekly + self.week

            index_content = self.indent + self.docs_path + str(self.end_date) + self.newline
            index_txt = index_content + index_txt

            contents = self.generate_contents()
            content_filename = self.docs_path + str(self.end_date) + self.docs_ext
            Utility.ensure_dir(content_filename)
            f = open (content_filename, "w")
            f.write(contents)
            f.close

            self.start_date = self.start_date + self.week

        self.index_txt = self.get_index_header() + index_txt

        f = open (self.index_filename, "w")
        f.write(self.index_txt)
        f.close

    def generate_contents(self):
        header = self.get_content_header()
        body = self.generate_content()
        return header + body

    def generate_content(self):
        width = 800
        height = 450
        start_date = str(self.start_date)
        end_date = str(self.end_date)

        number = "1"
        metric = "count"
        nodename = "india"
        platform = "eucalyptus"

        main_title =   self.newline + "Results for Eucalyptus on %(nodename)s.futuregrid.org" + self.newline + \
                    "-----------------------------------------------" + self.newline + \
                    ""
 
        src = "data/%(end_date)s/%(nodename)s/%(platform)s/%(metric)s/columnhighcharts.html"
        title = "Figure %(number)s. Total %(metric)s of VMs submitted per user for %(start_date)s  ~ %(end_date)s on %(nodename)s"
        content = main_title + self.get_content() % vars()
        content = content % vars()

        number = "2"
        metric = "runtime"

        content = content + (self.get_content() % vars()) % vars()

        number = 3
        metric = "count_node"

        src = "data/%(end_date)s/%(nodename)s/%(platform)s/%(metric)s/piehighcharts.html"
        title = "Figure %(number)s. Total VMs count per node cluster for %(start_date)s  ~ %(end_date)s on %(nodename)s"
 
        content = content + (self.get_content() % vars()) % vars()

        number = "4"
        metric = "count"
        nodename = "sierra"

        src = "data/%(end_date)s/%(nodename)s/%(platform)s/%(metric)s/columnhighcharts.html"
        title = "Figure %(number)s. Total %(metric)s of VMs submitted per user for %(start_date)s  ~ %(end_date)s on %(nodename)s"
 
        content = content + (main_title + self.get_content() % vars()) % vars()

        number = 5
        metric = "runtime"

        content = content + (self.get_content() % vars()) % vars()

        number = 6
        metric = "count_node"

        src = "data/%(end_date)s/%(nodename)s/%(platform)s/%(metric)s/piehighcharts.html"
        title = "Figure %(number)s. Total VMs count per node cluster for %(start_date)s  ~ %(end_date)s on %(nodename)s"
 
        content = content + (self.get_content() % vars()) % vars()

        return content

    def get_index_header(self):
        res =   "Cloud Metric Results" + self.newline + \
                "====================" + self.newline + \
                "We have collected cloud utilization data from Eucalyptus on FutureGrid such as India and Sierra resources and provide weekly and monthly reports to show usage of system resources measured by FG Cloud Metric." + self.newline + \
                self.newline + \
                "Contents:" + self.newline + \
                self.newline + \
                ".. toctree::" + self.newline + \
                self.indent + ":maxdepth: 1" + self.newline + \
                self.newline 
        return res

    def get_content_header(self):
        res =   self.start_date.strftime("%m/%d/%Y") + " - " + self.end_date.strftime("%m/%d/%Y") + self.newline + \
                "========================================" + self.newline
        return res
    
    def get_content(self):
        res =   "" + self.newline + \
                ".. raw:: html" + self.newline + \
                "" + self.newline + \
                self.indent + "<div style=\"margin-top:10px;\">" + self.newline + \
                self.indent + "<iframe width=\"%(width)s\" height=\"%(height)s\" src=\"%(src)s\" frameborder=\"0\"></iframe>" + self.newline + \
                self.indent + "</div>" + self.newline + \
                self.indent + "%(title)s" + self.newline
                
        return res

def main():
    result = Results()
    result.generate_index_and_contents()

if __name__ == "__main__":
    main()
