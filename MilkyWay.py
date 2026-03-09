import numpy as np
import glob
import re
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
import pandas as pd


c = 299792.458
f0 = 1420.40575
folder_name="Milky Way"
folder_name= input("Enter the folder name to process: ").strip()
degree_inclusion= input("Include only files with longitude in this range (e.g., -10,10) or press Enter to include all: ").strip()
if degree_inclusion:
    try:
        lon_min, lon_max = map(float, degree_inclusion.split(','))
        if lon_min > lon_max:
            print("Error: Minimum longitude must be less than maximum longitude.")
            exit(1)
    except ValueError:
        print("Error: Invalid input for longitude range. Please enter two numbers separated by a comma.")
        exit(1)
files = sorted(glob.glob(f"{folder_name}/*.cal.txt"))
if degree_inclusion:
    filtered_files = []
    for f in files:
        m = re.search(r"GLONG_(\d+)", f)
        if m:
            lon = float(m.group(1))
            if lon_min <= lon <= lon_max:
                filtered_files.append(f)
    files = filtered_files

longitudes = []
spectra = []
vel_axis = None

for f in files:
    m = re.search(r"GLONG_(\d+)", f)
    lon = float(m.group(1))
    longitudes.append(lon)

    # tsys= pd.


    # print(tsys)

    # print(f"Processing {f} with Tsys: {tsys}")

    # tsys_xx1 = tsys[0]
    # tsys_yy1 = tsys[1]
    # tsys_xx2 = tsys[2]
    # tsys_yy2 = tsys[3]



    data = np.loadtxt(f, comments='#')
    freq = data[:,0]
    
    xx = data[:,1]
    yy = data[:,2]
    freq2 = data[:,3] 
    X2 = data[:,4]
    Y2 = data[:,5]
   
    # I=(xx/tsys_xx1 + yy/tsys_yy1) / 2.0
    I1=(xx + yy) / 2.0
    I2=(X2 + Y2) / 2.0
    I = (I1 + I2) / 2.0

    vel1 = c * (f0 - freq) / f0
    vel2 = c * (f0 - freq2) / f0


    # vel_combined = np.concatenate([vel1, vel2]) 
    # I_combined = np.concatenate([I1, I2])
    vel_combined = vel1
    I_combined = I



    idx = np.argsort(vel_combined)
    vel_combined = vel_combined[idx]
    I_combined   = I_combined[idx]
    spectra.append(I_combined)
    if vel_axis is None:
        vel_axis = vel_combined


longitudes = np.array(longitudes)
spectra = np.array(spectra)
vel_axis = np.array(vel_axis)

idx = np.argsort(longitudes)
longitudes = longitudes[idx]
spectra = spectra[idx]

def find_terminal_velocity(vel, I, threshold_factor=0.25):
    peak = np.max(I)
    threshold = threshold_factor * peak


    mask = vel > 0
    vel_pos = vel[mask]
    I_pos = I[mask]

    good = np.where(I_pos > threshold)[0]
    if len(good) == 0:
        return np.nan

    return vel_pos[good].max()





terminal_velocities = [
    find_terminal_velocity(vel_axis, spec)
    for spec in spectra
]

plt.figure(figsize=(12,6))
plt.imshow(
    spectra.T,
    aspect='auto',
    origin='lower',
    extent=[longitudes.min(), longitudes.max(), vel_axis.min(), vel_axis.max()],
    cmap='inferno'
)
plt.xlabel("Galactic Longitude (deg)")
plt.ylabel("Velocity (km/s)")
plt.title("HI Galactic Plane: Longitude-Velocity Map")
plt.colorbar(label="Brightness")
plt.show()

#Limit velocities to -/+ 200 km/s for better visualization
plt.figure(figsize=(12,6))
plt.imshow(
    spectra.T,
    aspect='auto',
    origin='lower',
    extent=[longitudes.min(), longitudes.max(), -200, 200],
    cmap='inferno'
)
plt.xlabel("Galactic Longitude (deg)")
plt.ylabel("Velocity (km/s)")
plt.title("HI Galactic Plane: Longitude-Velocity Map (Zoomed)")
plt.colorbar(label="Brightness")
plt.show()


continue_analysis = input("Do you want to plot the rotation curve? (y/n): ").strip().lower()
if continue_analysis == 'y':
    R0 = 8.0
    Theta0 = 220

    l_rad = np.deg2rad(longitudes)
    R = R0 * np.sin(l_rad)
    Theta = np.array(terminal_velocities) + Theta0 * np.sin(l_rad)

    plt.figure()
    plt.scatter(R, Theta)
    plt.xlabel("Galactocentric Radius R (kpc)")
    plt.ylabel("Rotation Speed Θ(R) (km/s)")
    plt.title("Measured Galactic Rotation Curve")
    plt.grid(True)
    plt.show()

