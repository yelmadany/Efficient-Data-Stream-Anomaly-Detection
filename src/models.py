import data
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL

class STLModel:
    """
    STLModel class is designed to detect anomalies in a data stream using STL (Seasonal-Trend decomposition using LOESS).

    STL decomposition is chosen for its effectiveness in dealing seasonal components by separating them from the trend and residuals,
    making it suitable for data with seasonal patterns and potential anomalies. It adapts well to concept drift and 
    can handle both linear and non-linear trends, making it robust for real-time anomaly detection. In our simulated case,
    we are dealing with univariate data, which is ideal for STL as it can easily separate the components from each other.
    When compared to heavier models within the unsupervised scene, such an ensemble methods, STL provides a lightweight and efficient approach
    to detecting anomalies in our data. 

    Class Attributes:
        - data_points: Stores the incoming data points for analysis.
        - threshold_factor: Factor to determine the sensitivity of anomaly detection.
        - date: Current date index for the data stream.
        - anomalies: Series to store detected anomalies.
        - lower: Lower threshold for anomaly detection.
        - upper: Upper threshold for anomaly detection.
    """

    def __init__(self, threshold=3):
        self.data_points = []
        self.threshold_factor = threshold
        self.date = "1-1-2023"
        self.anomalies = pd.Series([])

    def fit(self):
        """
        Apply STL decomposition to the data points.
        Returns the fitted STL result.
        """
        stl = STL(self.data_points)
        res = stl.fit()
        return res

    def TrainSTLModel(self, instances):
        """
        Train the STL model with a given number of instances.
        Generates training data without contamination, fits the STL model,
        and calculates the residual mean and standard deviation to set the anomaly detection thresholds.
        If our data had a more varying trend, we could introduce retraining, however, the data remains static so 
        we it is not required for this use case.
        """
        #Generate training data without contamination
        trainingGenerator = data.generateCPUData(contamination=0, trainMode=True)
        
        #Create a time series index for the training data
        self.data_points = pd.Series(
            [next(trainingGenerator) for _ in range(instances)], 
            index=pd.date_range(self.date, periods=instances, freq="1h")
        )

        #Update the current date index 
        self.date = self.data_points.index[-1] + pd.Timedelta(1, "h")

        #Fit the STL model and calculate residual statistics
        result = self.fit()
        resid_mu = result.resid.mean()
        resid_dev = result.resid.std()

        #Set lower and upper thresholds for anomaly detection
        self.lower = resid_mu - self.threshold_factor * resid_dev
        self.upper = resid_mu + self.threshold_factor * resid_dev

    def predict(self, data, window_size):
        """
        Predict anomalies in the incoming data point and updates the data stream with the new data point.
        We refit the data with the new data point and check if the residual of the latest data point is outside the defined thresholds.
        If an anomaly is detected, it is recorded in the anomalies series of the class.
        """
        #Add new data point to the series
        new_point = pd.Series([data], index=[self.date])
        self.data_points = pd.concat([self.data_points, new_point])[-window_size:]
        
        #Update the current date index for the next point
        self.date = self.data_points.index[-1] + pd.Timedelta(1, "h")

        #refit the data
        result = self.fit()
        residual = result.resid[-1]

        #Anomaly detection: check Threshold Graph.png for reference
        if residual < self.lower or residual > self.upper:
            self.anomalies = pd.concat([self.anomalies, new_point])
            print(f"Anomaly detected at time {self.date}: {data}")

