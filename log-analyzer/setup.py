from setuptools import setup

import sys, os

version = '2.0.2.1'

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
    packages = ['futuregrid.eucalyptus.analyzer'],
    
    #include_package_data=True,
    #zip_safe=True,
    #install_requires=[
    #    # -*- Extra requirements: -*-
    #],
    
    entry_points={
        'console_scripts':
            [
             'fg-cleanup-table = futuregrid.eucalyptus.analyzer.fg-cleanup-table:main'
             'fg-euca-gather-log-files = futuregrid.eucalyptus.analyzer.fg-euca-gather-log-files:main'
             'fg-log-gz-decompressor = futuregrid.eucalyptus.analyzer.fg-log-gz-decompressor:main'
             'fg-parser = futuregrid.eucalyptus.analyzer.fg-parser:main'
             ]},
    
    install_requires = [
        'setuptools'
        ],
    
    )

# http://docs.python.org/distutils/introduction.html#distutils-simple-example
# http://docs.python.org/distutils/setupscript.html#setup-script
