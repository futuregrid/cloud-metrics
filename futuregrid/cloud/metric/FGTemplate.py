class HtmlTemplate:

    @staticmethod
    def index():
        return str(
	"""<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
	<html> <head>
	<title> %(title)s </title>
	</head>
	<body>
	<img src="https://portal.futuregrid.org/sites/default/files/u30/fg-logo-md.gif" width="94" height="65" alt="FutureGrid" /> Eucalyptus Monitor
	<h1> %(title)s </h1>
	<table>
	<tr>
	<td>
	<img src="pie.count.png" alt="chart" />
	</td>
	<td>
	<img src="bar.count.png" alt="chart" />
	</td>
	</tr>
	<tr>
	<td>
	Figure 1. Running instances per user of eucalyptus in India (pie chart)
	</td>
	<td>
	Figure 2. Running instances per user of eucalyptus in India (bar chart)
	</td>
	</tr>
	<tr>
	<td colspan="2">
	%(motion_chart)s
	</td>
	</tr>
	<tr>
	<td colspan="2">
	<br><br><br><br>
	Figure 3. Running instances per user of eucalyptus in India (motion chart)
	</td>
	</tr>
	<tr>
	<td>
	<img src="pie.sum.png" alt="chart" />
	</td>
	<td>
	<img src="bar.sum.png" alt="chart" />
	</td>
	</tr>
	<tr>
	<td>
	Figure 4. Runtime of instances per user of eucalyptus in India (pie type)
	</td>
	<td>
	Figure 5. Runtime of instances per user of eucalyptus in India (bar type)
	</td>
	</tr>
	</table>
	<hr>
	<address>Authors Hyungro Lee, Gregor von Laszewski, laszewski@gmail.com</address>
	<!-- hhmts start -->Last modified: %(now)s <!-- hhmts end -->
	</body> </html>""")

    @staticmethod
    def frame():
        return str(
        """<HTML>
            <HEAD> 
                <TITLE>FutureGrid Statistical reports</TITLE>
            </HEAD>
            <FRAMESET COLS="30%,70%">
                <FRAME scrolling=yes SRC="menu.html" NAME="left">
                <FRAME SRC="main.html" NAME="right">
            </FRAMESET>
        </HTML>
        """)

