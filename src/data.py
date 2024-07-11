import random
import time

def generateCPUData(contamination = 10, timeOfDay = 0, dayOfWeek = 0, trainMode = False):
  """
  The aim is to simulate CPU utilization of a company employee that works from 8am - 4pm, from monday to friday. 
  This employee leaves his device operational 24/7.
  As such, whenever he is not at the office, the computer should be in a downtime/idle where utilization does not exceed 10%.
  During office hours, utilization will increase and roam around 20% ~ 60%.
  The employee's boss has been upset as the employee has been playing video games on the job. So the boss wants to spy on the employee and ensure that his cpu usage never goes above 70% 

  This function attempts to simulate this activity, where each second in the real world, represents an hour in the employees life.
  This function is a generator that generates the CPU data as per request, while maintaining the state or in our case the time and week we are in.
  
  We also implement manual random noise to ensure the anomaly detection algorithm is operational.
  Contamination represents the likelyhood of a value streamed being contaimined.

  Parameters:
  - contaimination (int): Probability of anomalous generation (0 - 100)
  - timeOfDay (int): Current time of day (0-23).
  - dayOfWeek (int): Current dayOfWeek (0-6).
  - trainMode (bool): Flag to set the function to train mode (for fasting building)

  Yields the next instance of the data stream
  """ 
  while(True): #infinite loop as this is an infinite generator

    #Manual Contaimination
    contaimNumber = random.randint(1,100) #random num is picked from 1 to 100 
    if(contaimNumber > (100 - contamination)): #based on the desired contaimination parameter, we set the probability
      data = noiseData(timeOfDay, dayOfWeek)
    #Normal Data Generation 
    else:
      data = getData(timeOfDay, dayOfWeek)

    #-------Update parameters---------------
    timeOfDay = (timeOfDay + 1) % 24

    if(timeOfDay == 0): #update week
      dayOfWeek = (dayOfWeek + 1) % 7
    #---------------------------------------

    if(not trainMode): #during inital training phase we can skip the wait times 
        time.sleep(0.1) #sleep
    yield data
    
#-----------------------------------------------------------
def getData(timeOfDay, dayOfWeek, ):
  """
  Function is responsible for generating regular and seasonal data.
  Regular data: Downtime
  Seasonal data: Uptime (work hours) - Downtime(Weekends)

  Parameters:
  - timeOfDay (int): Current time of day (0-23).
  - dayOfWeek (int): Current dayOfWeek (0-6).

  Returns:
  - float: Simulated CPU utilization value.
  """
  #---------Get the Data----------------
  #Check if downtime (weekends or from 4pm to 8am)
  if(5 <= dayOfWeek < 7 or 0 <= timeOfDay < 8 or 17 <= timeOfDay < 24):  
     x = downTime()
  else:
     #else need to check other parameters before deciding
    x = upTime()

  return x
  #---------------------------------------


def noiseData(timeOfDay, dayOfWeek):
  """
  Function is responsible for generating irregular data/anomalies
  First identifies what is supposed to be the appropriate response and returns one of the other two responses.

  Parameters:
  - timeOfDay (int): Current time of day (0-23).
  - dayOfWeek (int): Current day (0-6).


  Returns:
  - float: Simulated anomalous CPU utilization value.
  """
  # print('Induced Anomaly: ')
  responses = [downTime, upTime, heavyLoad]
  if(5 <= dayOfWeek < 7 or 0 <= timeOfDay < 8 or 17 <= timeOfDay < 24):
    responses.remove(downTime)
  else:
    responses.remove(upTime)
  
  return random.choice(responses)() #Pick a random choice
  
#-----------------------------------------------------------

boundaries = "0110206070"

#------data events---------------------

def downTime():
  #downtime range from 1 - 10% (default)
  return random.uniform(int(boundaries[0:2]),int(boundaries[2:4])) 

def upTime():
  #uptime range from 20 - 60% (default)
  return random.uniform(int(boundaries[4:6]), int(boundaries[6:8]))

def heavyLoad():
    #HeavyLoad range from 70 - 100% (default)
  return random.uniform(int(boundaries[8:10]),100) 


#--------Extra Functions
def setboundaries(boundary):
  #Used to change the boundaries if desired
  boundaries = boundary
