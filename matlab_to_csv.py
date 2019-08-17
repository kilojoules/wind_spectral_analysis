import scipy.io
import pandas as pd
import sys
mn = sys.argv[-1]
mat = scipy.io.loadmat(mn)
mat = {k:v for k, v in mat.items() if k[0] != '_'}
data = pd.DataFrame({k: pd.Series(v[0]) for k, v in mat.items()})
data.to_csv("%s.csv" % mn[:-4])
