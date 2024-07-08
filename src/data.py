import random
import time



def generateCPUData(contamination = 10, index = 0, cycle = 0, EOM = False):
  """
  The aim is to simulate CPU utilization of a company employee that works from 8am - 4pm, from monday to friday. 
  This employee leaves his device operational 24/7.
  As such, whenever he is not at the office, the computer should be in a downtime/idle where utilization does not exceed 10%.
  During office hours, utilization will increase and roam around 10% ~ 70%.
  At the end of every month, the utilization is expected to significantly increase due to the employee's required data processing tasks.
  This function attempts to simulate this activity, where each second in the real world, represents an hour in the employees life.
  
  We also implement manual random noise to ensure the anomaly detection algorithm is operational.
  Contamination represents the likelyhood of a value streamed being contaimined.

  The function is built to run without the need to change any of the variables. However, the data generation may be tampered with if desired. 
  Check documentation.md for more information
  """ 

  contaimNumber = random.randint(1,100)

  if(contaimNumber > (100 - contamination)):
    data = noiseData(index, cycle, EOM)
  else:
    data = getData(index, cycle, EOM)

  #-------Update parameters---------------
  index = (index + 1) % 24

  if(index == 0): #update cycles
    cycle += 1

  if (cycle == 4):#update EOM
    EOM = True
  #---------------------------------------

  time.sleep(1) #sleep
  return data
    

#-----------------------------------------------------------
def getData(index, cycle, EOM):
  """
  Function is responsible for generating regular and seasonal data.
  Regular data: Downtime
  Seasonal data: Uptime (work hours) - Heavyload (End of the month) - Downtime(Weekends)
  """
  x = 0

  #---------Get the Data----------------
  #Check if downtime (weekends or from 4pm to 8am)
  if(5 <= cycle < 7 or 0 <= index < 8 or 17 <= index < 24):  
     x = downTime()
  else:
     #else need to check other parameters before deciding
    if(EOM): #if it is the end of the month, output heavy load
        x = heavyLoad()
    x = upTime()
  #---------------------------------------
  
  #-------Sleep and Return---------------
  return x


def noiseData(index, cycle, EOM):
  """
  Function is responsible for generating irregular data/anomalies
  First Identifies what is supposed to be the appropriate response and returns one of the other two responses.
  """
  print('Anomaly: ')
  responses = [downTime, upTime, heavyLoad]
  if(EOM):
    responses.remove(heavyLoad)
  elif(5 <= cycle < 7 or 0 <= index < 8 or 17 <= index < 24):
    responses.remove(downTime)
  else:
    responses.remove(upTime)
  
  return random.choice(responses)()
    

#-----------------------------------------------------------

#------data events

def downTime():
  #downtime range from 1 - 10% 
  return random.uniform(1,10) 

def upTime():
  #uptime range from 10 - 70% 
  return random.uniform(10, 70)

def heavyLoad():
    #HeavyLoad range from 70 - 100% 
  return random.uniform(70,100) 

