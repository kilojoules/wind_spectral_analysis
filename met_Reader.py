import io
import datetime
import requests
import pandas as pd
import calendar
import matplotlib.pyplot as plt
import numpy as np
baseStr = '09_29_2016_'
dat = pd.DataFrame()
for year in np.arange(2013, 2014):
    for month in range(1,2):
        httpFILE = 'http://wind.nrel.gov/MetData/135mData/M5Twr/20Hz/txt/%i_%s.txt'%(year, calendar.month_name[month])
        content = requests.get(httpFILE).content
        subdat = pd.read_csv(io.StringIO(content.decode('utf-8')), skiprows=[s for s in range(7)]+[8,9], sep=',')
        subdat.Date = pd.to_datetime(subdat.Date, format='%d-%m-%Y %H:%M:%S')
        dat = pd.concat([dat, subdat], ignore_index=True)

dat.to_csv('met_dat.csv', index=False)
