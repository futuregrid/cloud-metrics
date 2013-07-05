"""FutureGrid: Cloud Metrics

This project is the basis for providing several metrics as part of the
usage analysis of multiple cloud environments. 
"""

from setuptools import setup, find_packages
import sys, os

doclines = __doc__.split("\n")

######################################################################
# VERSION
######################################################################

try:
    version = open("VERSION.txt").read()
except:
    try:
        version = open("../VERSION.txt").read()
    except:
        version = "4.0.1"


######################################################################
# CLASSIFIER
######################################################################

classifiers = """\
Intended Audience :: Developers
Intended Audience :: Education
Intended Audience :: Science/Research
Development Status :: 3 - Alpha
Intended Audience :: Developers
License :: OSI Approved :: Apache Software License
Programming Language :: Python
Topic :: Database
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: POSIX :: Linux
Programming Language :: Python :: 2.7
Operating System :: MacOS :: MacOS X
Topic :: Scientific/Engineering
Topic :: System :: Clustering
Topic :: System :: Distributed Computing
"""

######################################################################
# VERSION CHECK
######################################################################

if sys.version_info < (2, 7):
    _setup = setup
    def setup(**kwargs):
        if kwargs.has_key("classifiers"):
            del kwargs["classifiers"]
        _setup(**kwargs)

#DISTUTILS_DEBUG=1

######################################################################
# REQUIREMENTS
######################################################################

requires = [
    'setuptools',
    'pip',
    'sphinxcontrib-issuetracker',
    'sphinxcontrib-googlechart',
    'cherrypy',
    'pymongo',
    'cmd2',
    'pygooglechart',
    'sqlalchemy',
    'mysql-connector-python',
    'mysql-python',
    'pymongo',
    'mimerender'
    ],

install_requires = []

for package in requires:
    try:
        import package
    except ImportError:
        install_requires.append(package)

######################################################################
# SETUP
######################################################################

setup(
    name='fgmetric',
    version=version,
    description=doclines[0],
    long_description = "\n".join(doclines[2:]),
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='FutureGrid Eucalyptys Log File Analysis',
    author='Gregor von Laszewski, Hyungro Lee, Fugang Wang',
    maintainer='Gregor von Laszewski, Hyungro Lee',
    maintainer_email="laszewski@gmail.com",
    author_email='laszewski@gmail.com',
    url='https://github.com/futuregrid/futuregrid-cloud-metrics',
    license='Apache 2.0',
    package_dir = {'': 'src'},
    packages = find_packages('src',exclude=['ez_setup', 'examples', 'tests']),
    #include_package_data=True,
    #zip_safe=True,
    
    entry_points={
        'console_scripts':
            [
             #'fg-cleanup-db = fgmetric.shell.FGEucaMetricsDB:command_clean_database',
             'fg-euca-gather-log-files = fgmetric.shell.FGCollectFiles:main',
             'fg-parser = fgmetric.shell.FGParser:main',
             'fg-logparser = fgmetric.shell.FGLogParser:main',
             'fg-metric-converter = fgmetric.shell.FGConverter:main',
             #'fg-metric-old = fgmetric.shell.FGAnalyzer:main',
             'fg-metric = fgmetric.shell.FGMetricShell:main',
             'fg-metric-install = fgmetric.setup.FGInstall:main'
             # TODO: fg-metric-install will be merged into fg-metric subshell
             ]},

        install_requires=install_requires
    )

    # Removed console script
    # 'fg-log-gz-decompressor = futuregrid.eucalyptus.analyzer.FGLogGzDecompressor:main',


# http://docs.python.org/distutils/introduction.html#distutils-simple-example
# http://docs.python.org/distutils/setupscript.html#setup-script
# http://mxm-mad-science.blogspot.com/2008/02/python-eggs-simple-introduction.html
