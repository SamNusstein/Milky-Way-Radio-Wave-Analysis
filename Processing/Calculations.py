import numpy as np
import pandas as pd
def calculate_galactic_rotation(highest_freq_df):
    R0 = 8500       # pc
    V0 = 220        # km/s
    f0 = 1420.40575177  # MHz
    c  = 299792.458     # km/s

    l_rad = np.deg2rad(highest_freq_df['Longitude'])
    v_lsr = c * ((f0 - highest_freq_df['Highest_freq']) / highest_freq_df['Highest_freq'])
    R = R0 * np.abs(np.sin(l_rad))
    V = v_lsr.to_numpy() + V0 * np.sin(l_rad)
    return R, V



def calculate_mass_radius(R, V):
    G   = 6.67e-11
    pc  = 3.086e16
    R_m = R * pc
    V_ms= V * 1000
    m_gal = (V_ms**2 * R_m) / G
    return m_gal