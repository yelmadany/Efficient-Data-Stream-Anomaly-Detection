#custom build modules
import data
import models

#External Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import matplotlib.dates as mdates
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parameterValidation(iterations, contamination, window_size, trainIterations):
    """
    This function validates the parameters for the visualizeData function.

    - iterations, window_size, and trainIterations must be positve integers
    - contaimation must be an integer from 0 to 100 inclusive
    - lastly, window_size must be > than trainIterations in order to avoid losing out on any of the train data.
    """
    if not isinstance(iterations, int) or iterations < 0:
        raise ValueError("iterations must be a positive integer.")

    if not isinstance(window_size, int) or window_size < 0:
        raise ValueError("window_size must be a positive integer.")

    if not isinstance(trainIterations, int) or trainIterations < 0:
        raise ValueError("trainIterations must be a positive integer.")
    
    if not isinstance(contamination, int) or not (0 <= contamination <= 100):
        raise ValueError("contamination must be a number between 0 and 100.")

    if window_size < trainIterations:
        raise ValueError("window_size cannot be less than trainIterations.")

def visualizeData(iterations=150, contamination=10, window_size=10000, trainIterations=3000):
    """
    This function is responsible for creating the real-time visualization graph that displays
    the real-time data stream and any detected anomalies from the chosen algorithm
    
    Parameters:
    - iterations: Number of data points to simulate in the system, default is 150
    - contamination: Probability of a data point being anomalous (0-100)
    - window_size: Number of data points the model holds before dropping old points (must be > trainIterations)
    - trainIterations: Number of points to generate as base data to "train" the model (must be > 0)

    This function outputs a matplotlib graph that updates every second.
    """
    try:
        # Validate parameters to ensure they are compatible
        parameterValidation(iterations, contamination, window_size, trainIterations)
        
        logging.info("Starting data visualization with parameters - iterations: %d, contamination: %f, window_size: %d, trainIterations: %d", iterations, contamination, window_size, trainIterations)

        # Create the plot
        fig, ax = plt.subplots()
        plt.get_current_fig_manager().canvas.manager.set_window_title('Anomaly Detection')

        # Create and train the model
        model = models.STLModel()
        model.TrainSTLModel(trainIterations)

        #Creating the generator that will generate the data stream for us, with a certain contaimination percentage
        realTimeGenerator = data.generateCPUData(contamination=contamination)

        def stop(event):
            """
            This function activates when clicking the stop button in the graph. 
            Stops the animation.
            """
            ani.event_source.stop()
            logging.info('Stopping animation...')

        def update(frame):
            """
            This function is responsible for generating, predicting, and displaying the results of our system while allowing for
            the animation to occur. 

            This function is called by the FuncAnimation function, which is provided by the matplotlib library.
            """
            try:
                #Generate new data point and predict 
                data_point = next(realTimeGenerator)
                model.predict(data_point, window_size)

                #replot the graph
                ax.clear()
                ax.set_ylim([0, 100]) #As we are plotting CPU utilization, the y-axis has a range of [0-100]
                ax.plot(model.data_points.index[trainIterations:], model.data_points[trainIterations:], label="Data Stream", color="blue")

                #If we have anomalies, we need to plot it in the appropriate indices
                if len(model.anomalies):
                    ax.scatter(model.anomalies.index , model.anomalies, color='red', marker='D', label='Anomalies')

                #Labelling the graph
                ax.legend()
                ax.set_title("Real-Time Data Stream and Anomaly Detection")
                ax.set_xlabel("Time")
                ax.set_ylabel("CPU Utilization")
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            except Exception as e:
                logging.error("Error during update: %s", e)

        # Create a stop button
        stop_button_ax = plt.axes([0.88, 0.01, 0.10, 0.075])
        stop_button = Button(stop_button_ax, 'Stop')
        stop_button.on_clicked(stop) #calls the stop function from earlier

        ani = animation.FuncAnimation(fig, update, frames=iterations, repeat=False)
        plt.show() #shows the plot

    except ValueError as ve:
        logging.error("Parameter validation error: %s", ve)
    except Exception as e:
        logging.error("Unexpected error: %s", e)