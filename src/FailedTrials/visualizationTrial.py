import matplotlib.pyplot as plt
import data
import numpy as np
import matplotlib.animation as animation
from matplotlib.widgets import Button
import time

def visualizeData(iterations = 10):
  fig, ax = plt.subplots()
  realTimeGenerator = data.generateCPUData(contamination= 10) #can set the contaimination probability
  data_points = []
  stopped = False

  # def stop():
  #   ani.event_source.stop()
  #   print('Attempting to stop')

  def update(frame):
    global stopped
    data = next(realTimeGenerator)
    data_points.append(data)
    
    ax.clear()
    axs = plt.gca()
    # ax.set_xlim([xmin, xmax])
    axs.set_ylim([0, 100])
    ax.plot(data_points, label="Data Stream")
    ax.legend()
    ax.set_title("Real-Time Data Stream and Anomaly Detection")
    ax.set_xlabel("Time")
    ax.set_ylabel("CPU Utilization")
  
    loc = fig.add_axes([0.9, 0.05, 0.1, 0.075])
    bstop = Button(loc, 'Stop')
    bstop.on_clicked(stop(ani))

  ani = animation.FuncAnimation(fig, update, frames=iterations, repeat=False,interval = 100)
  plt.show()

visualizeData()