import os
import scipy
import io
import datetime
import requests
import urllib.request as rq
import pandas as pd
import calendar
import matplotlib.pyplot as plt
import numpy as np
# https://wind.nrel.gov/MetData/135mData/M5Twr/20Hz/mat/2018/06/06/06_06_2018_00_00_00_000.mat
STDS = []
NORMS = []
                                
dat = pd.DataFrame()
for year in np.arange(2018, 2019):
    for month in [7]:
    #for month in range(1, 12):
        #for day in range(1, 30):
        for day in [20, 21]:
        #for day in calendar.monthrange(year, month):
           for hour in range(0, 24):
               for minute in [0, 10, 20, 30, 40, 50]:
                   time = '%02d_%02d_00_000' % (hour, minute)
                   httpFILE = 'http://wind.nrel.gov/MetData/135mData/M5Twr/20Hz/mat/%i/%02d/%02d/%02d_%02d_%i_%s.mat' % (year, month, day, month, day, year, time)
           #httpFILE = 'http://wind.nrel.gov/MetData/135mData/M5Twr/20Hz/mat/%i/%2i/%2i_%2i_%i_%s.mat' % (year, calendar.month_name[month], calendar.month_name[month], day, year, time)
                   print(httpFILE)
                   fln = httpFILE.split(os.sep)[-1]
                   rq.urlretrieve(httpFILE, '.' + os.sep + fln)
                   #os.popen("wget %s" % httpFILE)
                   #os.system("wget -c --read-timeout=5 --tries=0 %s" % httpFILE)
           #content = requests.get(httpFILE).content
                   mat = scipy.io.loadmat(fln)
                   mat = {k:v for k, v in mat.items() if k[0] != '_'}
                   data = pd.DataFrame({k: pd.Series(v[0]) for k, v in mat.items()})
                   subdat = pd.DataFrame({'u122': data.Cup_WS_122m.values[0][0][:, 0], 'u82':data.Cup_WS_C1_80m.values[0][0][:, 0]})
                   if subdat.u82.mean() < 6: continue
                   alphs = np.log(122. / 82.)/ np.log(subdat.u122 / np.log(subdat.u82)) 
                   alphs = alphs[alphs > -3]
                   alphs = alphs[alphs < 5]
                   plt.hist(alphs, 100)
                   plt.title('%.2f m/s' % subdat.u82.mean())
                   plt.savefig(fln[:-4] + '_hist')
                   plt.clf()
                   STDS.append(np.std(alphs))

                   alphs -= np.mean(alphs)
                   alphs /= np.std(alphs)
                   NORMS.extend(alphs)
plt.hist(NORMS, 100)
plt.savefig('norm')
plt.clf()
