import data
import numpy as np
from joblib import load

# load the model
model = load('./src/models/madModel.joblib')

realTimeGenerator = data.generateCPUData(contamination= 10) #can set the contaimination probability

while(True):
  datapoint = np.array(next(realTimeGenerator)).reshape(-1,1)
  is_outlier = model.predict(datapoint)
  score = model.decision_function(datapoint)
  
  print('Outlier:', is_outlier)
  print('Score', score)


