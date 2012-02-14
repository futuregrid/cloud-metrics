#! /usr/bin/env python

import os

from GChartWrapper import Pie3D

G = Pie3D([5,10]).title('Hello Pie').color('red','lime').label('hello', 'world')
G.color('green')

os.system ("open -a /Applications/Safari.app " + '"' + str(G) + '"')
