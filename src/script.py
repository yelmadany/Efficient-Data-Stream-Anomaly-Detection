import visualization as v
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_user_input(prompt, default):
    #Function used to get the user input for the different parameters.
    user_input = input(prompt)
    return int(user_input) if user_input else default


#There are three methods of starting the system

#Method 1: using default values, if the user does not provide any values
iterations, contamination, window_size, trainIterations = 150, 10, 10000, 3000


if len(sys.argv) > 1: #Method 2: Through the command line
    # If parameters are passed via command line arguments
    try:
        iterations = int(sys.argv[1])
        contamination = int(sys.argv[2])
        window_size = int(sys.argv[3])
        trainIterations = int(sys.argv[4])
    except (IndexError, ValueError):
        logging.error("Invalid command line arguments. Using default values.")

else:
    # Ask the user if they want to input parameters
    use_defaults = input("Do you want to use default values? (yes/no): ").strip().lower()
    
    if use_defaults == 'no': #Method 3: Through user input
        iterations = get_user_input("Enter iterations (default 150): ", 150)
        contamination = get_user_input("Enter contamination (0-100, default 10): ", 10)
        window_size = get_user_input("Enter window_size (default 10000): ", 10000)
        trainIterations = get_user_input("Enter trainIterations (default 3000): ", 3000)

v.visualizeData(iterations=iterations, contamination=contamination, window_size=window_size, trainIterations=trainIterations)