import pandas as pd
import numpy as np
import matplotlib.dates as md
from scipy.stats import norm
import matplotlib
import matplotlib.pyplot as plt
dat = pd.read_csv('./met_dat.csv')
dat = dat[dat.index < 500]
dat.alpha = np.log(dat['Speed Ux (sonic_100m)'] / dat['Speed Ux (sonic_41m)']) / np.log(100/41)
dat.alpha[dat.alpha < -1] = np.nan
dat.alpha[dat.alpha == 0] = np.nan
dat.alpha[dat.alpha > 3] = np.nan
if False:
   f, ax = plt.subplots(figsize=(100, 5))
   xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
   ax.xaxis.set_major_formatter(xfmt)
   ax.plot_date(dat.Date, dat.alpha)
   ax.set_xticklabels(dat.Date[::2])
   plt.savefig('shears.pdf', bbox_to_inches='tight')
   plt.clf()
   plt.close('all')

deltas = []
for ii in range(dat.alpha.size - 1):
    deltas.append(dat.alpha[ii+1] - dat.alpha[ii])
plt.hist(deltas, 50, normed=True)
x = np.linspace(-2, 2, 1000)
plt.plot(x, norm.pdf(x, 0, .15))
plt.savefig('deltas.pdf')
plt.clf()
