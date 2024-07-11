import data
import numpy as np
from pyod.models.mad import MAD
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
from statsmodels.tsa.seasonal import STL
import matplotlib.pyplot as plt
from datetime import datetime

#Train Data Creation
trainingGenerator = data.generateCPUData(contamination = 10, trainMode=True)
cpuData = []

for i in range(2977):
  cpuData.append(next(trainingGenerator))

datas = pd.Series(cpuData, index=pd.date_range(start = "1-1-2023", end = "5-5-2023", freq="1h"))

stl = STL(cpuData)
res = stl.fit()




# fig = res.plot()
# fig.savefig("image2.png")

estimated = res.seasonal + res.trend
plt.figure(figsize=(12,4))
plt.plot(datas)
plt.plot(estimated)

plt.savefig('estVSact.png')
#Anomaly Detection
resid_mu = res.resid.mean()
resid_dev = res.resid.std()

lower = resid_mu - 3*resid_dev
upper = resid_mu + 3*resid_dev

plt.figure(figsize=(10,4))
plt.plot(res.resid)

plt.fill_between([datetime(2023,1,1), datetime(2023,1,5)], lower, upper, color='g', alpha=0.25, linestyle='--', linewidth=2)
plt.xlim(datetime(2023,1,1), datetime(2023,1,5))

plt.savefig('Test.png')

anomalies = datas[(res.resid < lower) | (res.resid > upper)]

plt.figure(figsize=(10,4))
plt.plot(datas)
plt.axvline(datetime(2023,1,1), color='k', linestyle='--', alpha=0.5)
    
plt.scatter(anomalies.index, anomalies, color='r', marker='D')
plt.savefig('dssddsf.png')

# month_deviations = datas.groupby(lambda d: d.hour).std()

# plt.figure(figsize=(10,4))
# plt.plot(month_deviations)
# plt.title('Deviation by Month', fontsize=20)
# plt.ylabel('CPU', fontsize=16)

# plt.savefig('byMonth.png')
