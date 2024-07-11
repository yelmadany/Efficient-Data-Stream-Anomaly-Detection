To whomever may read this,

I hope you are having a great day.

<hr>
This project contains three folders.

**docs**: contains the project requirements and gives u an indication of what the project should do, I was planning on adding detailed documentation but I ran out of time

**graphs**: contains a few graphs showcasing how my algorithm works in detecting anomalies. Essentially boils down to adjusting the data for seasonality then identifying if the residual is within the allowed threshold or not.

**src**: This is where the source code lies. I've split the code into 4 files. <br>
        &emsp; -data.py: contains all the code related to data generation.<br>
        &emsp; -models.py: contains the anomaly detection algorithm(STL) coded in OOP style.<br>
        &emsp; -visualization.py: contains the code to visualize the data in real time, using matplotlib.<br>
        &emsp; -script.py: this is the file used in order to actually run the project.
<br><br>
I also included some of my failed trials and test code in the FailedTrials folder.
<hr>

**Starting the project**
There's a total of three way of starting the project, all of them involve the terminal.

1. Running script.py with no parameters and answering yes, this should start the program with the default parameters: (150, 10, 10000, 3000).

2. Running scripty.py with terminal parameters, four parameters are required: [iterations (positve integer), contamination(integer with range(0 - 100)), window_size(postive integer > than trainIterations), trainIterations(positive integer)], you can find more information about these parameters below.

3. Running script.py with no parameters, but this time answering no. This will allow you to see exactly which parameters you are adjusting 

<hr>

**Parameters**:
- iterations: Number of data points to simulate in the system, default is 150

- contamination: Probability of a data point being anomalous (0-100)

- window_size: Number of data points the model holds before dropping old points (must be > trainIterations)

- trainIterations: Number of points to generate as base data to "train" the model (must be > 0)


<hr>

Thank you for reading. Have a good day!