import os
import numpy as np
from scipy.optimize import curve_fit

# Function to extract data from a file
def extract_data(file_path):
    steps = []
    volume = []
    potential_energy = []
    dihedral = []
    enthalpy = []
    msd_all = []
    msd_oxy = []
    msd_hydro = []

    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  # Skip the first line (header)
        for line in lines:
            data = line.split()
            if len(data) < 8:
                continue  # Skip lines that do not have enough data
            steps.append(float(data[0]))
            volume.append(float(data[1]))
            potential_energy.append(float(data[2]))
            dihedral.append(float(data[3]))
            enthalpy.append(float(data[4]))
            msd_all.append(float(data[5]))
            msd_oxy.append(float(data[6]))
            msd_hydro.append(float(data[7]))

    return steps, volume, potential_energy, dihedral, enthalpy, msd_all, msd_oxy, msd_hydro

def linear(x, a, b):
    return a * x + b

# Get a list of all folders in the current directory
folders = [folder for folder in os.listdir() if os.path.isdir(folder)]

# Initialize dictionaries to store average data
averages = {}  # Dictionary to store averages for each folder

# Create a text file to store the results
output_file_path = 'averages.txt'
with open(output_file_path, 'w') as output_file:

    # Write the header for the output file
    output_file.write("#Folder\tTemperature (K)\tPressure (atm)\tAverage Volume\tAverage Potential Energy\tAverage Dihedral\tHeat capacity\tCompressibility\tDiffusionCoeff\tAverage Enthalpy\n")

    # Loop through folders, process data, and calculate averages
    for folder in folders:
        folder_parts = folder.split('_')
        if len(folder_parts) != 2:
            continue  # Skip folders that do not have the expected format (e.g., '100K_5000atm')

        temperature_str, pressure_str = folder_parts
        if not temperature_str.endswith('K') or not pressure_str.endswith('atm'):
            continue  # Skip folders that do not have the expected suffixes

        try:
            temperature = float(temperature_str[:-1])  # Remove 'K' from temperature string
            pressure = float(pressure_str[:-3])  # Remove 'atm' from pressure string
        except ValueError:
            continue  # Skip this folder if the conversion fails

        # Check if thermo.txt exists in the folder
        file_path = os.path.join(folder, 'thermo.txt')
        if not os.path.exists(file_path):
            continue  # Skip this folder if thermo.txt doesn't exist

        # Load data from the thermo.txt file in the folder
        data = extract_data(file_path)

        # Assign individual lists to variables
        steps, vol, pe, dihedral, enthalpy, c_3, c_4, c_5 = data

        # Check if the data lists are empty
        if not steps or not vol or not pe or not dihedral or not enthalpy or not c_3:
            continue  # Skip this folder if any of the data lists are empty

        # K_b
        k = 8.314462618 * 1.e-3  # kJ/(mol K)

        # Calculate the averages
        num_molecules = 64

        if ((temperature > 450 and temperature < 850 and pressure < 15) or (temperature in [450, 550, 650] and pressure in [500]) or (temperature == 500 and pressure == 100) or (temperature == 600 and pressure == 100)):
            num_molecules = 64 * 8


        avg_vol = np.mean(np.array(vol) / num_molecules)
        avg_pe = np.mean(np.array(pe) / num_molecules)
        avg_enthalpy = np.mean(np.array(enthalpy) / num_molecules)
        avg_dihedral = np.mean(dihedral)
        heat_cap = np.var(np.array(enthalpy) / num_molecules) * np.power(4.184, 2) / (k * temperature**2)
        compres = np.var(np.array(vol) / num_molecules) / (k * temperature * avg_vol)
        popt, pcov = curve_fit(linear, 6 * 0.0005 * np.array(steps), c_3)
        diff = popt[0]

        # Store the averages in the dictionary
        averages[folder] = {
            'Temperature (K) from Folder': temperature,
            'Pressure (atm)': pressure,
            'Average Volume': avg_vol,
            'Average Potential Energy': avg_pe,
            'Average Dihedral': avg_dihedral,
            'Heat capacity': heat_cap,
            'Compressibility': compres,
            'Diffusion Coefficient': diff,
            'Average Enthalpy': avg_enthalpy
        }

        # Write the average data to the text file
        output_file.write(f"{folder}\t{averages[folder]['Temperature (K) from Folder']}\t{averages[folder]['Pressure (atm)']}\t{averages[folder]['Average Volume']}\t{averages[folder]['Average Potential Energy']}\t{averages[folder]['Average Dihedral']}\t{averages[folder]['Heat capacity']}\t{averages[folder]['Compressibility']}\t{averages[folder]['Diffusion Coefficient']}\t{averages[folder]['Average Enthalpy']}\n")

