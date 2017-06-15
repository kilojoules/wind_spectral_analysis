import scipy.fftpack
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
dat = pd.read_csv('./met_dat.csv')
N = len(dat[u'Speed (cup_ 130 m)'])
xf = np.linspace(0.0, 1e4, N//2)
plt.plot(xf, 2.0/N * np.abs(scipy.fftpack.fft(dat[u'Speed (cup_ 130 m)'][:N//2])))
plt.show() 
