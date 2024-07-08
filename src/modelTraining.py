import data
import numpy as np
from joblib import dump
from pyod.models.mad import MAD

#Initial training of the model on data with no contaimination and we enable trainMode to speedup the type
trainingGenerator = data.generateCPUData(contamination = 0, trainMode=True)
Training_Data = []

for i in range(10000):
  Training_Data.append(next(trainingGenerator))

Training_Data = np.array(Training_Data, ).reshape(-1,1)

madModel = MAD(contamination=0.1)
madModel.fit(Training_Data)

# save the model
dump(madModel, './src/models/madModel.joblib')
