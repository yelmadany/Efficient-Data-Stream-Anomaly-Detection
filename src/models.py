import data
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL

class STLModel():
# OOP style Model that maintains the state of the data
  def __init__(self, threshold = 3):
    self.data_points = []
    self.threshold_factor = threshold
    self.date = "1-1-2023"
    self.anomalies = pd.Series([])

  # Calculate Residual Mean and Standard Deviation for Anomaly Detection
  def fit(self):
    stl = STL(self.data_points)
    res = stl.fit()

    return res

  def TrainSTLModel(self, instances):
    # Train Data Creation
    trainingGenerator = data.generateCPUData(contamination=0, trainMode=True)  # No contamination for training data
    
    self.data_points = pd.Series([next(trainingGenerator) for _ in range(instances)], index=pd.date_range(self.date,periods=instances, freq="1h"))

    self.date = self.data_points.index[-1] + pd.Timedelta(1, "h")

    result = self.fit()
    resid_mu = result.resid.mean()
    resid_dev = result.resid.std()
    self.lower = resid_mu - self.threshold_factor * resid_dev
    self.upper = resid_mu + self.threshold_factor * resid_dev


  def predict(self, data, window_size):
    new_point = pd.Series([data], index=[self.date])
    self.data_points = pd.concat([self.data_points, new_point])[-window_size:]
    self.date = self.data_points.index[-1] + pd.Timedelta(1, "h")

    if len(self.data_points) > window_size:
        self.data_points.pop(0)
  
    result = self.fit()

    residual = result.resid[-1]

    if residual < self.lower or residual > self.upper:
        self.anomalies = pd.concat([self.anomalies, new_point])
        print(f"Anomaly detected at time {self.date}: {data}")