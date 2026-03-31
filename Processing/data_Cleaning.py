import glob
import re
import numpy as np
import pandas as pd

def load_data(path, f0, c):

    files = sorted(glob.glob(f"{path}/*.cal.txt"))
    if not files:
        raise FileNotFoundError(f"No .cal.txt files found in the directory: {path}")    
    dfs = []
    intensities={}
    freq = None
    for f in files:
        m = re.search(r"GLONG[_-](\d+)", f)
        if m is None:
            continue
        lon = int(m.group(1))

        data = np.loadtxt(f, comments="#")

        if freq is None:
            freq = data[:, 0]
            vel = c * (f0 - freq) / f0


        xx = data[:, 1]
        yy = data[:, 2]
        intensities[lon] = (xx + yy) / 2.0
    all_dfs = pd.DataFrame(intensities)
    all_dfs.insert(0, "Velocity", vel)
    all_dfs.insert(0, "Frequency", freq)
    all_dfs = all_dfs[['Frequency', 'Velocity'] + [i for i in sorted(intensities) if i in all_dfs.columns]]
    
    return all_dfs
