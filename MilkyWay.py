import numpy as np
import glob
import re
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import RectBivariateSpline
import progressbar



c = 299792.458
f0 = 1420.40575
path="Milky Way"

files = sorted(glob.glob(f"{path}/*.cal.txt"))

filtered_files = []
for f in files:
    m = re.search(r"GLONG_(\d+)", f)
    if m:
        lon = float(m.group(1))
        filtered_files.append(f)
    files = filtered_files
filtered_files=filtered_files.sort(key=lambda x: float(re.search(r"GLONG_(\d+)", x).group(1)))

longitudes = []
spectra = []
vel_axis = None
temp=pd.DataFrame()



        

for f in files:
    m = re.search(r"GLONG_(\d+)", f)
    lon = float(m.group(1))
    longitudes.append(lon)

    data = np.loadtxt(f, comments='#')
    freq = data[:,0]
    
    xx = data[:,1]
    yy = data[:,2]
    I=(xx + yy) / 2.0
    if len(temp) == 0:
        temp = pd.DataFrame({'Frequency': freq, 'Intensity'+' '+str(lon): I})
    else:
        temp['Intensity'+' '+str(lon)] = I

    spectra.append(I)
    if vel_axis is None:
        vel = c * (f0 - freq )/ f0
        vel_axis = vel
        temp['Velocity'] = vel

temp = temp[['Frequency', 'Velocity'] + [col for col in temp.columns if col.startswith('Intensity')]]
temp.set_index(['Frequency','Velocity'],inplace=True,append=True)
ahhh=pd.DataFrame()
progress=progressbar.ProgressBar(maxval=(90*920))
progress.start()
total=0
for col in temp.columns:
    app=[]

    for i in range(len(temp[col])-1):
        app.append(np.abs(temp[col].loc[i]-temp[col].loc[i+1]))
        total+=1
        progress.update(total)
    ahhh[col]=app
progress.finish()

print(ahhh.max())

longitudes = np.array(longitudes)
spectra = np.array(spectra)
vel_axis = np.array(vel_axis)
   
idx = np.argsort(longitudes)
longitudes = longitudes[idx]
spectra = spectra[idx]

#get row for max frequency :)
v_r=temp    


def find_v_r(vel_axis, spectra):


    return vel_axis[np.argmax(spectra, axis=1)]



#Limit velocities to -/+ 200 km/s for better visualization
vel_mask = (vel_axis >= -200) & (vel_axis <= 200)
vel_axis_zoom = vel_axis[vel_mask]
spectra_zoom = spectra[:, vel_mask]

plt.figure(figsize=(12,6))
plt.imshow(
    spectra_zoom.T,
    aspect='auto',
    origin='lower',
    extent=[longitudes.min(), longitudes.max(), vel_axis_zoom.min(), vel_axis_zoom.max()],
    cmap='inferno')
plt.xlabel("Galactic Longitude (deg)")
plt.ylabel("Velocity (km/s)")
plt.title("HI Galactic Plane: Longitude-Velocity Map (Zoomed)")
plt.colorbar(label="Brightness")
plt.show()


continue_analysis = input("Do you want to plot the rotation curve? (y/n): ").strip().lower()
if continue_analysis == 'y':
    R0 = 8000 #pc
    V0=220 #km/s

    R = R0 * np.sin(longitudes)
    V = np.array(find_v_r(vel_axis, spectra)) + V0 * np.sin(longitudes)

    plt.figure()
    plt.scatter(R, V)
    plt.xlabel("Galactocentric Radius R (pc)")
    plt.ylabel("Rotation Speed V(R) (km/s)")
    plt.title("Measured Galactic Rotation Curve")
    plt.grid(True)
    plt.show()

