# keep the following two lines as is
import matplotlib
matplotlib.use('TkAgg')

from pylab import *

n = 160
p=0.25

def init():
    global config, nextconfig
    config = zeros([n,n]) ## matrix n by n of zeroes
    nextconfig = zeros([n,n])
    for x in xrange(n):
        for y in xrange(n):
            config[x,y] = 1 if random () < p else 0

def update():
    global config, nextconfig
    for x in xrange(n):
        for y in xrange(n):
            c= sum(config[(x+dx)%n,(y+dy)%n] for dx in [-1,0,1] for dy in [-1,0,1]) 
            # use c and config[x,y]
            nextconfig[x,y]= 1 if c > 3 else 0
            # Calculate values in next config
    config, nextconfig = nextconfig, config
            
            #for dx in range(-1, 1+1)
             #   for dy in range(-1,1+1)

def observe():
    imshow(config)

import pycxsimulator
pycxsimulator.GUI(title='My Simulator',interval=0, parameterSetters = []).start(func=[init,observe,update])
# 'title', 'interval' and 'parameterSetters' are optional
