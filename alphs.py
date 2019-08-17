import pandas as pd
import numpy as np
import matplotlib.dates as md
from scipy.stats import norm
import matplotlib
import matplotlib.pyplot as plt
dat = pd.read_csv('./met_dat.csv')
dat = dat[dat.index < 500]
dat = dat[dat['Speed Ux (sonic_100m)'] != -999]
dat = dat[dat['Speed Ux (sonic_41m)'] != -999]
dat['alpha'] = np.log(dat['Speed Ux (sonic_100m)'] / dat['Speed Ux (sonic_41m)']) / np.log(100/41)
dat = dat[ dat.alpha > -1]
dat = dat[dat.alpha < 3]
dat = dat[dat.alpha != 0]
dat.reset_index(inplace=True)
#dat.alpha[dat.alpha < -1] = np.nan
#dat.alpha[dat.alpha == 0] = np.nan
#dat.alpha[dat.alpha > 3] = np.nan
#matplotlib.rcParams.update({'font.size': 12})
if True:
   fig, ax = plt.subplots(3, figsize=(10, 5), sharex=True)
   xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
   ax[0].plot_date(dat.Date[:100], dat.alpha[:100])
   #ax[2].get_xaxis().set_major_formatter(xfmt)
   #ax[2].set_xticklabels(dat.Date[:50][::2])
   ax[1].plot(dat['Speed Ux (sonic_100m)'][:100])
   ax[2].plot(dat['Speed Ux (sonic_41m)'][:100])
   ax[0].set_ylabel('Calculated Shear')
   ax[1].set_ylabel('Measured Speed at 100 m')
   ax[2].set_ylabel('Measured Speed at 41 m')
   fig.autofmt_xdate(rotation=25)
   plt.savefig('sheartime.pdf', bbox_to_inches='tight')
   plt.clf()
   plt.close('all')

plt.hist(dat.alpha, 100)
plt.xlabel('shear')
plt.savefig('shears.pdf')
plt.clf()

plt.hist(dat['Ti (cup_ 122 m) QC']) 
plt.savefig('tis.pdf')
plt.clf()

deltas = []
for ii in range(dat.alpha.size - 1):
    deltas.append(dat.alpha[ii+1] - dat.alpha[ii])
plt.hist(deltas, 100, normed=True)
x = np.linspace(-2, 2, 1000)
plt.plot(x, norm.pdf(x, 0, .15))
plt.xlabel('change in shear between ten minute periods')
plt.savefig('deltas.pdf')
plt.clf()
print("DELTA STD IS ", np.std(deltas))
print("SHEAR STD IS ", np.std(dat.alpha))
