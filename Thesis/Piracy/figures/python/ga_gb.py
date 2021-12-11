#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 29 May 2019
@author: Ole Peters
"""
import matplotlib.pyplot as plt
import numpy as np

x0=np.arange(1,100000,1)
t0=0
ta=1
tb=2
#x0=1000
Dxa=1000
Dxb=2500
r=.03


ga=1/(ta-t0)*np.log(1+(Dxa/(x0*np.exp(r*(ta-t0)))))+r
gb=1/(tb-t0)*np.log(1+(Dxb/(x0*np.exp(r*(tb-t0)))))+r

plt.plot(x0,ga-gb,linestyle='-',color='blue')
#plt.plot(x0,gb,linestyle='-',color='red')
plt.rc('xtick',labelsize=16)
plt.rc('ytick',labelsize=16)

plt.plot([0, 50000], [0, 0], 'k--', lw=1)
plt.xlabel('$x(t_0)$ (dollars)',fontsize=16)
plt.ylabel('$g_a-g_b$ (per annum)',fontsize=16)

plt.xlim(0,30000)
plt.xticks([0,10000,20000,30000])
plt.ylim(-.02,.02)
plt.savefig("./../ga_gb.pdf", bbox_inches='tight')
plt.show()
