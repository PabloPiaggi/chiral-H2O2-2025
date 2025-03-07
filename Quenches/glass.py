import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

################################
# Variables
################################
enthalpy_column = 4
window_size = 3000
Tmax = 400
Tmin = 100
total_steps=1000000000
stride=100
# Low T interval
min_temp1 = 100
max_temp1 = 250
# High T interval
min_temp2 = 250
max_temp2 = 400
# List of pressures - See filename below to choose this properly
pressures = np.array([0, 1000, 2000,3000,4000,5000,6000,7000,8000,9000,10000])
# Plot True or False
plot_flag = False
################################

################################
# Some checks
################################
if min_temp1 > max_temp1:
    raise ValueError("min_temp1 must be smaller than max_temp1")
if min_temp2 > max_temp2:
    raise ValueError("min_temp2 must be smaller than max_temp2")
if max_temp1 > min_temp2:
    raise ValueError("max_temp1 must be smaller than min_temp2")
################################

#print("Pressures", "T_g")

################################
# Loop over pressures
################################
for press in pressures:
    # Load file
    filename = str(press) + "atm_1/thermo.txt"
    data = np.genfromtxt(filename)
    total_lines = len(data)
    data[:, 0] = Tmax + (Tmin - Tmax) * data[:, 0]/float(total_steps)
    if window_size > (total_lines - 1):
        raise ValueError("window_size = " + str(window_size) + " is < or = to the total lines = " + str(
            total_lines) + " in the file" + filename)
    # Calculate mean values of temperature and enthalpy for different windows
    mean_temperatures = np.array([np.mean(data[i:(i + window_size), 0]) for i in np.arange(0, total_lines, window_size)])
    mean_enthalpy = np.array([np.mean(data[i:(i + window_size), enthalpy_column]) for i in np.arange(0, total_lines, window_size)])
    # Fit straight lines to the mean values above
    # Low T fit
    region1 = np.logical_and(mean_temperatures > min_temp1, mean_temperatures < max_temp1)
    reg1 = LinearRegression().fit(mean_temperatures[region1].reshape(-1, 1), mean_enthalpy[region1])
    # High T fit
    region2 = np.logical_and(mean_temperatures > min_temp2, mean_temperatures < max_temp2)
    reg2 = LinearRegression().fit(mean_temperatures[region2].reshape(-1, 1), mean_enthalpy[region2])
    # Find crossing point between straight lines
    dummy_temperature = np.linspace(min_temp1, max_temp2, 10000)
    predict_low = reg1.predict(dummy_temperature.reshape(-1, 1))
    predict_high = reg2.predict(dummy_temperature.reshape(-1, 1))
    # Find points used for low T fit and high T fit
    points_low_T_fit = np.column_stack((mean_temperatures[region1], mean_enthalpy[region1]))
    points_high_T_fit = np.column_stack((mean_temperatures[region2], mean_enthalpy[region2]))
    ################################
    # Plot
    ################################
    if plot_flag == True:
         #plt.scatter(points_low_T_fit[:, 0], points_low_T_fit[:, 1], label='Low T Data', color='cyan')
         plt.scatter(points_low_T_fit[::stride, 0], points_low_T_fit[::stride, 1], label='Low T Data', color='cyan')
         plt.scatter(points_high_T_fit[::stride, 0], points_high_T_fit[::stride, 1], label='High T Data', color='orange')
         #Plot the fitted lines
         plt.plot(dummy_temperature, predict_low, label='Low T Fit', color='blue')
         plt.plot(dummy_temperature, predict_high, label='High T Fit', color='red')
         plt.legend()
         plt.title(f"{press} atm")
         plt.xlabel("T [K]")
         plt.ylabel("H [kcal]")
         plt.show()
     #print(press, crossing_temperature)
     # Final Data
    crossing_temperature = dummy_temperature[np.argmin(np.abs(predict_low - predict_high))]
    with open("glasstransition.txt", "a") as file:
         file.write(f"{press} {crossing_temperature}\n")
