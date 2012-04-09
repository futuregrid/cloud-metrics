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
	<img src="pie.png" alt="chart" />
	</td>
	<td>
	<img src="bar.png" alt="chart" />
	</td>
	</tr>
	<tr>
	<td>
	Figure 1. Running instances per user of eucalyptus in India (pie type)
	</td>
	<td>
	Figure 2. Running instances per user of eucalyptus in India (bar type)
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
            <FRAMESET COLS="11%,89%">
                <FRAME scrolling=yes SRC="menu.html" NAME="left">
                <FRAME SRC="main.html" NAME="right">
            </FRAMESET>
        </HTML>
        """

