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


b_u=1
C=1
x=np.arange(-.1,2.,.01)

t0=0
ta=1.3
tb=2
x0=0
Dxa=1.4
Dxb=3
tPR=(Dxa*tb-Dxb*ta)/(Dxa-Dxb)

#Payouts
plt.plot([ta, ta], [x0, x0+Dxa], 'k-', lw=3)
plt.plot([tb, tb], [x0, x0+Dxb], 'k-', lw=3)

#wealth levels
plt.plot([-.3, 2.5], [x0, x0], 'k:', lw=1)
plt.plot([-.3, 2.5], [x0+Dxa, x0+Dxa], 'k:', lw=1)
plt.plot([-.3, 2.5], [x0+Dxb, x0+Dxb], 'k:', lw=1)
#
plt.rc('xtick',labelsize=16)
plt.rc('ytick',labelsize=16)
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')
#plt.xlabel('$t$',fontsize=16)
#plt.ylabel('Payment',fontsize=16)
plt.xticks([t0,ta,tb], ['$t_0$','$t_a$','$t_b$'], rotation=0)
plt.yticks([x0,x0+Dxa,x0+Dxb], ['$x(t_0)$','$x(t_0)+\Delta x_a$','$x(t_0)+\Delta x_b$'], rotation=0)
plt.xlim(-.3,2.5)
plt.ylim(-.5,3.3)
plt.savefig("./../setup.pdf", bbox_inches='tight')
plt.show()
