class FGReports():

    """ 
    FutureGrid Reports Generator
    ============================

    This module creates cmd command files to execute fg-metric.
    Using python vars(), this module assigns strings to variables in template files.
    The replaced contents will be saved as cmd command files in destination directory.
    The cmd command files are ready to be executed with pipe in fg-metric shell. 

    ---------------------------------
    Usage: python generate_reports.py
    ---------------------------------

    --------------
    Required files
    --------------
    weekly.template, monthly.template, ...

    ------
    Output
    ------
    weekly_reports/2012-01-01.txt, ...

    """


    """ UNDER DEVELOPMENT. BELOW FUNCTIONS ARE NOT TESTED. """
    def __init__(self):
        self.load_period()
        self.load_clouds()
        self.load_nodes()
        self.load_vars()

    def load_period(self):
        self.period = [ "weekly", "monthly", "quarterly" ]

    def load_clouds(self):
        self.clouds = [ "eucalyptus", "openstack", "nimbus" ]

    def load_nodes(self):
        self.nodes = [ "india", "sierra", "foxtrot", "alamo", "hotel" ]

    def load_vars(self):
        """Set vars for cmd command files. These vars will be replaced in template"""

        self.data = { "start_date": None,
                        "end_date": None,
                        "hostname": None,
                        "period": None,
                        "timetype": None,
                        "metric": None,
                        "groups": None }

    def get_clouds(self):
        return self.clouds

    def get_nodes(self):
        return self.nodes

    def get_template(self, node, cloud):
        filename = self.get_template_path(node, cloud)
        content = fgets(filename)
        filled_content = content % vars(self.data)

    def generate(self):
        for node in self.get_nodes():
            for cloud in self.get_clouds():
                template = self.get_template(node, cloud)
                self.create_cmd_file(template)

if __name__ == "__main__":
    fgreport = FGReports()
    fgreport.generate()
