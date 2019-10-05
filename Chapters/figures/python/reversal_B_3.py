#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 10:54:25 2018

@author: obp48
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from matplotlib.ticker import NullFormatter
plt.ion()

fig1, ax1 = plt.subplots()

t0=0
ta=1
tb=2
x0=5000
Dxa=1000
Dxb=2500
r=.03

xta=x0*np.exp(r*(ta-t0))+Dxa
xtb=x0*np.exp(r*(tb-t0))+Dxb


#Payouts
plt.plot([ta, ta], [x0, xta], 'b-', lw=3)
plt.plot([tb, tb], [x0, xtb], 'r-', lw=3)

#wealth levels
plt.plot([-.3, 2.5], [x0, x0], 'k:', lw=1)
plt.plot([-.3, 2.5], [xta, xta], 'k:', lw=1)
plt.plot([-.3, 2.5], [xtb, xtb], 'k:', lw=1)

#slopes
plt.plot([t0,ta], [x0, xta], 'b:', lw=2)
plt.plot([t0,tb], [x0, xtb], 'r:', lw=2)

plt.rc('xtick',labelsize=16)
plt.rc('ytick',labelsize=16)
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')
#plt.xlabel('$t$',fontsize=16)
#plt.ylabel('Payment',fontsize=16)
plt.yscale('log')
ax1.yaxis.set_major_formatter(NullFormatter())
ax1.yaxis.set_minor_formatter(NullFormatter())
plt.xticks([t0,ta,tb], ['$t_0$','$t_a$','$t_b$'], rotation=0)
plt.yticks([x0,x0+Dxa,x0+Dxb], ['$x(t_0)>x(t_0)^{PR}$','$x(t_a)$','$x(t_b)$'], rotation=0)
plt.xlim(-0.2,2.5)
plt.ylim(x0,xtb*1.03)
plt.savefig("./../reversal_B_3.pdf", bbox_inches='tight')
plt.show()
