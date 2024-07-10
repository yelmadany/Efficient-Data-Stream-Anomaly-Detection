import data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import models

# Define the real-time visualization function
def visualizeData(iterations=1000, contamination=10, window_size=10000, trainIterations = 3000):
    fig, ax = plt.subplots()
    realTimeGenerator = data.generateCPUData(contamination=contamination)
    model = models.STLModel()
    model.TrainSTLModel(trainIterations)

    def stop(event):
        ani.event_source.stop()
        print('Stopping animation...')

    def update(frame):
        data = next(realTimeGenerator)
        model.predict(data, window_size)

        ax.clear()
        ax.set_ylim([0, 100])
        ax.plot(model.data_points[trainIterations:], label="Data Stream", color="blue")

        if len(model.anomalies):
            ax.scatter(model.anomalies.index, model.anomalies, color='red', marker='D', label='Anomalies')

        ax.legend()
        ax.set_title("Real-Time Data Stream and Anomaly Detection")
        ax.set_xlabel("Time")
        ax.set_ylabel("CPU Utilization")

    # Create a stop button
    stop_button_ax = plt.axes([0.9, 0.05, 0.1, 0.075])
    stop_button = Button(stop_button_ax, 'Stop')
    stop_button.on_clicked(stop)

    ani = animation.FuncAnimation(fig, update, frames=iterations, repeat=False)
    plt.show()