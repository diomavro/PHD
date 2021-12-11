import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime

t0 = 0
ta = 1.3
tb = 2
x0 = 0
Dxa = 1.4
Dxb = 3
tPR = (Dxa*tb-Dxb*ta)/(Dxa-Dxb)

f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))

#Payouts
ax1.plot([ta, ta], [x0, x0+Dxa], 'b-', lw=3)
ax1.plot([tb, tb], [x0, x0+Dxb], 'r-', lw=3)

#wealth levels
ax1.plot([-.3, 2.5], [x0, x0], 'k:', lw=1)
ax1.plot([-.3, 2.5], [x0+Dxa, x0+Dxa], 'k:', lw=1)
ax1.plot([-.3, 2.5], [x0+Dxb, x0+Dxb], 'k:', lw=1)

#initial slopes
ax1.plot([t0,ta], [x0, x0+Dxa], 'b:', lw=2)
ax1.plot([t0,tb], [x0, x0+Dxb], 'r:', lw=2)

#reversed slopes
plt.sca(ax1)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')
plt.xticks([t0, ta, tb], ['$t_0<t_0^{PR}$', '$t_a$', '$t_b$'], rotation=0)
plt.yticks([x0, x0+Dxa, x0+Dxb], ['$x(t_0)$', '$x(t_0)+\Delta x_a$', '$x(t_0)+\Delta x_b$'], fontsize=10, rotation=90)
plt.xlim(-.3, 2.4)
plt.ylim(-.5, 3.3)

#Payouts
ax2.plot([ta, ta], [x0, x0+Dxa], 'b-', lw=3)
ax2.plot([tb, tb], [x0, x0+Dxb], 'r-', lw=3)

#wealth levels
ax2.plot([-.3, 2.5], [x0, x0], 'k:', lw=1)
ax2.plot([-.3, 2.5], [x0+Dxa, x0+Dxa], 'k:', lw=1)
ax2.plot([-.3, 2.5], [x0+Dxb, x0+Dxb], 'k:', lw=1)

#indifference slopes
ax2.plot([tPR,ta], [x0, x0+Dxa], 'b:', lw=2)
ax2.plot([tPR,tb], [x0, x0+Dxb], 'r:', lw=2)

plt.sca(ax2)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')
plt.xticks([tPR, ta, tb], ['$t_0=t_0^{PR}$', '$t_a$', '$t_b$'], rotation=0)
plt.yticks([x0, x0+Dxa, x0+Dxb], ['$x(t_0)$', '$x(t_0)+\Delta x_a$', '$x(t_0)+\Delta x_b$'], fontsize=10, rotation=90)
plt.xlim(-.3, 2.4)
plt.ylim(-.5, 3.3)

#Payouts
ax3.plot([ta, ta], [x0, x0+Dxa], 'b-', lw=3)
ax3.plot([tb, tb], [x0, x0+Dxb], 'r-', lw=3)

#wealth levels
ax3.plot([-.3, 2.5], [x0, x0], 'k:', lw=1)
ax3.plot([-.3, 2.5], [x0+Dxa, x0+Dxa], 'k:', lw=1)
ax3.plot([-.3, 2.5], [x0+Dxb, x0+Dxb], 'k:', lw=1)

#reversed slopes
ax3.plot([(tPR+ta)/2,ta], [x0, x0+Dxa], 'b:', lw=2)
ax3.plot([(tPR+ta)/2,tb], [x0, x0+Dxb], 'r:', lw=2)
plt.sca(ax3)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')
plt.xticks([(tPR+ta)/2, ta, tb], ['$t_0>t_0^{PR}$', '$t_a$', '$t_b$'], rotation=0)
plt.yticks([x0, x0+Dxa, x0+Dxb], ['$x(t_0)$', '$x(t_0)+\Delta x_a$', '$x(t_0)+\Delta x_b$'], fontsize=10, rotation=90)
plt.xlim(-.3, 2.4)
plt.ylim(-.5, 3.3)
plt.savefig("./reversals.eps", bbox_inches='tight')
plt.show()