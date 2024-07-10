#libraries
import data
import numpy as np
from pyod.models.mad import MAD
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
from statsmodels.tsa.seasonal import STL
import matplotlib.pyplot as plt

class RealTimeSTLAnomalyDetector:
    def __init__(self, window_size=48, seasonal=7, threshold=3):
        self.window_size = window_size
        self.seasonal = seasonal
        self.threshold = threshold
        self.data_window = []
        self.stl = None
        self.std_dev = None

    def fit(self, initial_data):
        self.data_window = initial_data
        self.stl = STL(self.data_window, seasonal=self.seasonal).fit()
        self.std_dev = np.std(self.stl.resid)

    def predict(self, new_data_point):
        #self.data_window.append(new_data_point)
        self.data_window = pd.concat([self.data_window, new_data_point], ignore_index=True)
        if len(self.data_window) > self.window_size:
            self.data_window.pop(0)

        if len(self.data_window) == self.window_size:
            self.stl = STL(self.data_window, seasonal=self.seasonal).fit()
            residual = self.stl.resid.iloc[-1]
            is_anomaly = abs(residual) > self.threshold * self.std_dev
            self.std_dev = np.std(self.stl.resid)  # Update std_dev with the new residuals
            return is_anomaly
        else:
            return False
        
        
stl = RealTimeSTLAnomalyDetector()

#Train Data Creation
trainingGenerator = data.generateCPUData(contamination = 10, trainMode=True)
Training_Data = []

for i in range(8761):
  Training_Data.append(next(trainingGenerator))

datas = pd.Series(Training_Data, index=pd.date_range(start = "1-1-2023", end = "1-1-2024", freq="1h"))

stl.fit(datas)

realTimeGenerator = data.generateCPUData(contamination= 10)

def dateGenerator():
  X = pd.date_range(start = "1-1-2023", end = "1-1-2024", freq="1h")
  for date in X:
     yield date


Dates = dateGenerator()
for i in range(100):
  datapoint = pd.Series(next(realTimeGenerator), index=[next(Dates)])
  is_anomaly = stl.predict(datapoint)

  if(is_anomaly):
      print("Anomaly Detected")


def plot_real_time_data(real_time_data, detector):
    fig, ax = plt.subplots()
    anomalies = [point if detector.predict(point) else None for point in real_time_data]

    ax.plot(real_time_data, label="Data Stream")
    ax.plot(anomalies, 'ro', label="Anomalies")
    ax.legend()
    ax.set_title("Real-Time Data Stream and Anomaly Detection")
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    plt.show()

plot_real_time_data(real_time_data, stl)






# stl = STL(data, seasonal=7)
# res = stl.fit()
# fig = res.plot()
# fig.savefig("image.png")


