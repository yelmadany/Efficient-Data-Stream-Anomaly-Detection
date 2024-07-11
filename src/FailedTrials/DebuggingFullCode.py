import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from statsmodels.tsa.seasonal import STL
import random
import time

def generateCPUData(contamination = 10, timeOfDay = 0, week = 0, EOM = False, trainMode = False):
  """
  The aim is to simulate CPU utilization of a company employee that works from 8am - 4pm, from monday to friday. 
  This employee leaves his device operational 24/7.
  As such, whenever he is not at the office, the computer should be in a downtime/idle where utilization does not exceed 10%.
  During office hours, utilization will increase and roam around 10% ~ 70%.
  At the end of every month, the utilization is expected to significantly increase due to the employee's required data processing tasks.
  This function attempts to simulate this activity, where each second in the real world, represents an hour in the employees life.

  This function is a generator that generates the CPU data as per request, while maintaining the state or in our case the time and week we are in.
  
  We also implement manual random noise to ensure the anomaly detection algorithm is operational.
  Contamination represents the likelyhood of a value streamed being contaimined.

  The function is built to run without the need to change any of the variables. However, the data generation may be tampered with if desired. 
  Check documentation.md for more information
  """ 

  while(True): #infinite loop as this is an infinite generator

    #Manual Contaimination
    contaimNumber = random.randint(1,100) #random num is picked from 1 to 100 
    if(contaimNumber > (100 - contamination)): #based on the desired contaimination parameter, we set the probability
      data = noiseData(timeOfDay, week, EOM)

    #Normal Data Generation 
    else:
      data = getData(timeOfDay, week, EOM)

    #-------Update parameters---------------
    timeOfDay = (timeOfDay + 1) % 24

    if(timeOfDay == 0): #update week
      week = (week + 1) % 7

    # if (week == 4):#update EOM
    #   EOM = True
    #---------------------------------------

    if(not trainMode): #during inital training phase we can skip the wait times 
        time.sleep(0.1) #sleep
    yield data
    
#-----------------------------------------------------------
def getData(timeOfDay, week, EOM):
  """
  Function is responsible for generating regular and seasonal data.
  Regular data: Downtime
  Seasonal data: Uptime (work hours) - Heavyload (End of the month) - Downtime(Weekends)

  Parameters:
  - timeOfDay (int): Current time of day (0-23).
  - week (int): Current week (0-6).
  - EOM (bool): End of month indicator.

  Returns:
  - float: Simulated CPU utilization value.
  """
  #---------Get the Data----------------
  #Check if downtime (weekends or from 4pm to 8am)
  if(5 <= week < 7 or 0 <= timeOfDay < 8 or 17 <= timeOfDay < 24):  
     x = downTime()
  else:
     #else need to check other parameters before deciding
    if(EOM): #if it is the end of the month, output heavy load
        x = heavyLoad()
    x = upTime()

  return x
  #---------------------------------------


def noiseData(timeOfDay, week, EOM):
  """
  Function is responsible for generating irregular data/anomalies
  First Identifies what is supposed to be the appropriate response and returns one of the other two responses.

  Parameters:
  - timeOfDay (int): Current time of day (0-23).
  - week (int): Current week (0-6).
  - EOM (bool): End of month indicator.

  Returns:
  - float: Simulated anomalous CPU utilization value.
  """
  # print('Induced Anomaly: ')
  responses = [downTime, upTime, heavyLoad]
  if(EOM):
    responses.remove(heavyLoad)
  elif(5 <= week < 7 or 0 <= timeOfDay < 8 or 17 <= timeOfDay < 24):
    responses.remove(downTime)
  else:
    responses.remove(upTime)
  
  return random.choice(responses)()
  
#-----------------------------------------------------------


#------data events---------------------

def downTime():
  #downtime range from 1 - 10% 
  return random.uniform(1,10) 

def upTime():
  #uptime range from 15 - 55% 
  return random.uniform(15, 55)

def heavyLoad():
    #HeavyLoad range from 70 - 100% 
  return random.uniform(70,100) 


#----- Additional Functions




def fit(data):
  stl = STL(data)
  res = stl.fit()

  return res

def TrainSTLModel(instances):
  # Train Data Creation
  trainingGenerator = generateCPUData(contamination=0, trainMode=True)  # No contamination for training data
  cpuData = pd.Series([next(trainingGenerator) for _ in range(instances)], index=pd.date_range("1-1-2023",periods=instances, freq="1h"))

    # Initial STL Decomposition
  return fit(cpuData), cpuData


def predict(data, data_points, anomalies, window_size):
    new_data_index = data_points.index[-1] + pd.Timedelta(hours=1)
    new_data_series = pd.Series([data], index=[new_data_index])
    data_points = pd.concat([data_points, new_data_series])
    
    if len(data_points) > window_size:
        data_points = data_points[-window_size:]

    if len(data_points) >= window_size:
        res = fit(data_points)

        residual = res.resid.iloc[-1]
        if residual < lower or residual > upper:
            anomalies.append((data_points.index[-1], data))
            print(f"Anomaly detected at {data_points.index[-1]}: {data}")
    else:
        res = fit(data_points)
    
    return res, data_points







# Define the real-time visualization function
def visualizeData(iterations=10, contamination=10, window_size=100):
    fig, ax = plt.subplots()
    realTimeGenerator = generateCPUData(contamination=contamination)
    _, updated_data_points = TrainSTLModel(1000)
    anomalies = []

    def stop(event):
        ani.event_source.stop()
        print('Stopping animation...')

    def update(frame):
        data = next(realTimeGenerator)
        res, _ = predict(data, updated_data_points, anomalies, window_size)
        ax.clear()
        ax.set_ylim([0, 100])
        ax.plot(updated_data_points, label="Data Stream", color="blue")

        if len(updated_data_points) >= window_size:
            ax.plot(updated_data_points.index[-window_size:], res.trend + res.seasonal, label="Estimated", color="orange")
            if anomalies:
                anomaly_indices, anomaly_values = zip(*anomalies)
                ax.scatter(anomaly_indices, anomaly_values, color='red', marker='D', label='Anomalies')

        ax.legend()
        ax.set_title("Real-Time Data Stream and Anomaly Detection")
        ax.set_xlabel("Time")
        ax.set_ylabel("CPU Utilization")

    # Create a stop button
    stop_button_ax = plt.axes([0.9, 0.05, 0.1, 0.075])
    stop_button = Button(stop_button_ax, 'Stop')
    stop_button.on_clicked(stop)

    ani = animation.FuncAnimation(fig, update, frames=iterations, repeat=False, interval=1000)
    plt.show()

model, datax = TrainSTLModel(1000)
# Calculate Residual Mean and Standard Deviation for Anomaly Detection
resid_mu = model.resid.mean()
resid_dev = model.resid.std()
threshold_factor = 2
lower = resid_mu - threshold_factor * resid_dev
upper = resid_mu + threshold_factor * resid_dev
visualizeData(iterations=100, contamination=10, window_size=100)