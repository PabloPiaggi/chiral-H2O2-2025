import numpy as np
import matplotlib.pyplot as plt

################################
# Variables
################################
# Change column to the one of the order parameter
order_parameter_column = 3
# Choose the number of last steps reasonably
number_of_last_steps = 10000
# List of pressures - See filename below to choose this properly
pressures = np.array([5000,6000])
# List of instances - this affects the filename below
instances = np.arange(1,61)
################################

################################
# Loop over pressures
################################
for press in pressures:
    list_avg_final_order_parameter = []
    for instance in instances:
        # Load file
        filename = str(press) + "atm_" + str(instance) + "/thermo.txt"
        data = np.genfromtxt(filename)
        # Average of last steps for one file
        avg_final_order_parameter = np.mean(data[-number_of_last_steps:, order_parameter_column])
        #list_avg_final_order_parameter.append(avg_final_order_parameter)
        with open("phi_med_new.txt", "a") as file:
            file.write(f"{press} {avg_final_order_parameter}\n")

