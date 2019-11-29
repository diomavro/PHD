import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from matplotlib.ticker import NullFormatter
plt.ion()

f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(17, 4))

t0 = 0
ta = 1
tb = 2
x0 = 500
Dxa = 1000
Dxb = 2500
r = .03

xta = x0*np.exp(r*(ta-t0))+Dxa
xtb = x0*np.exp(r*(tb-t0))+Dxb

ax1.plot([ta, ta], [x0, xta], 'b-', lw=3)
ax1.plot([tb, tb], [x0, xtb], 'r-', lw=3)
ax1.plot([-.3, 2.5], [x0, x0], 'k:', lw=1)
ax1.plot([-.3, 2.5], [xta, xta], 'k:', lw=1)
ax1.plot([-.3, 2.5], [xtb, xtb], 'k:', lw=1)
ax1.plot([t0,ta], [x0, xta], 'b:', lw=2)
ax1.plot([t0,tb], [x0, xtb], 'r:', lw=2)
plt.sca(ax1)
plt.rc('xtick',labelsize=10)
plt.rc('ytick',labelsize=10)
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')
plt.yscale('log')
ax1.yaxis.set_major_formatter(NullFormatter())
ax1.yaxis.set_minor_formatter(NullFormatter())
plt.xticks([t0, ta, tb], ['$t_0$', '$t_a$', '$t_b$'], rotation=0)
plt.yticks([x0, x0+Dxa, x0+Dxb], ['$x(t_0)<x(t_0)^{PR}$', '$x(t_a)$', '$x(t_b)$'], fontsize=10, rotation=90)
plt.xlim(-0.2, 2.5)
plt.ylim(x0, xtb*1.03)


t0 = 0
ta = 1
tb = 2
x0 = 2277
Dxa = 1000
Dxb = 2500
r = .03

xta = x0*np.exp(r*(ta-t0))+Dxa
xtb = x0*np.exp(r*(tb-t0))+Dxb

ax2.plot([ta, ta], [x0, xta], 'b-', lw=3)
ax2.plot([tb, tb], [x0, xtb], 'r-', lw=3)
ax2.plot([-.3, 2.5], [x0, x0], 'k:', lw=1)
ax2.plot([-.3, 2.5], [xta, xta], 'k:', lw=1)
ax2.plot([-.3, 2.5], [xtb, xtb], 'k:', lw=1)
ax2.plot([t0,ta], [x0, xta], 'b:', lw=2)
ax2.plot([t0,tb], [x0, xtb], 'r:', lw=2)
plt.sca(ax2)
plt.rc('xtick',labelsize=10)
plt.rc('ytick',labelsize=10)
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')
plt.yscale('log')
ax2.yaxis.set_major_formatter(NullFormatter())
ax2.yaxis.set_minor_formatter(NullFormatter())
plt.xticks([t0, ta, tb], ['$t_0$', '$t_a$', '$t_b$'], rotation=0)
plt.yticks([x0, x0+Dxa, x0+Dxb], ['$x(t_0)=x(t_0)^{PR}$', '$x(t_a)$', '$x(t_b)$'], fontsize=10, rotation=90)
plt.xlim(-0.2, 2.5)
plt.ylim(x0, xtb*1.03)


t0 = 0
ta = 1
tb = 2
x0 = 5000
Dxa = 1000
Dxb = 2500
r = .03

xta = x0*np.exp(r*(ta-t0))+Dxa
xtb = x0*np.exp(r*(tb-t0))+Dxb

ax3.plot([ta, ta], [x0, xta], 'b-', lw=3)
ax3.plot([tb, tb], [x0, xtb], 'r-', lw=3)
ax3.plot([-.3, 2.5], [x0, x0], 'k:', lw=1)
ax3.plot([-.3, 2.5], [xta, xta], 'k:', lw=1)
ax3.plot([-.3, 2.5], [xtb, xtb], 'k:', lw=1)
ax3.plot([t0,ta], [x0, xta], 'b:', lw=2)
ax3.plot([t0,tb], [x0, xtb], 'r:', lw=2)
plt.sca(ax3)
plt.rc('xtick',labelsize=10)
plt.rc('ytick',labelsize=10)
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')
plt.yscale('log')
ax3.yaxis.set_major_formatter(NullFormatter())
ax3.yaxis.set_minor_formatter(NullFormatter())
plt.xticks([t0, ta, tb], ['$t_0$', '$t_a$', '$t_b$'], rotation=0)
plt.yticks([x0, x0+Dxa, x0+Dxb], ['$x(t_0)>x(t_0)^{PR}$', '$x(t_a)$', '$x(t_b)$'], fontsize=10, rotation=90)
plt.xlim(-0.2, 2.5)
plt.ylim(x0, xtb*1.03)

plt.savefig("./reversals_B.eps", bbox_inches='tight')