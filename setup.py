try:
	    from setuptools import setup, find_packages
except ImportError:
	    from distutils.core import setup

import sys, os

version = '2.0.2.2'

#DISTUTILS_DEBUG=1

setup(
    name='futuregrid.euca.analyzer',
    version=version,
    description="The package allows the analysis of Eucalyptus logs and display the information graphically",
    long_description="""\
The package allows the analysis of Eucalyptus logs and display the information graphically""",
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='FutureGrid Eucalyptys Log File Analysis',
    author='Gregor von Laszewski',
    author_email='laszewski@gmail.com',
    url='http://futuregrid.org',
    license='Apache 2.0',
    package_dir = {'': '.'},
    #packages = ['futuregrid.eucalyptus.analyzer', 'futuregrid.eucalyptus.analyzer.lib'],
    packages = find_packages(),
    
    #include_package_data=True,
    #zip_safe=True,
    #install_requires=[
    #    # -*- Extra requirements: -*-
    #],
    
    entry_points={
        'console_scripts':
            [
             'fg-cleanup-db = futuregrid.eucalyptus.analyzer.FGEucaMetricsDB:command_clean_database',
             'fg-euca-gather-log-files = futuregrid.eucalyptus.analyzer.FGEucaGatherLogFiles:main',
             'fg-parser = futuregrid.eucalyptus.analyzer.FGParser:main'
             ]},
    
    install_requires = [
        'setuptools',
        'cmd2'
        ],
    )

    # Removed console script
    # 'fg-log-gz-decompressor = futuregrid.eucalyptus.analyzer.FGLogGzDecompressor:main',


# http://docs.python.org/distutils/introduction.html#distutils-simple-example
# http://docs.python.org/distutils/setupscript.html#setup-script
# http://mxm-mad-science.blogspot.com/2008/02/python-eggs-simple-introduction.html
