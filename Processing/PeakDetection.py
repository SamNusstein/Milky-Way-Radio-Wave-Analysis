from scipy.ndimage import gaussian_filter1d
import numpy as np
def get_peak_frequency(sigma,spectra,lon,freq_axis):
    if lon >16:
        thresh=.40
        sigma=3
    else:
        thresh=.45
        sigma=1.75
        
    smooth = gaussian_filter1d(spectra, 3)

    n_edge = int(len(smooth) * thresh)
    edge_data = np.concatenate([smooth[:n_edge], smooth[-n_edge:]])
    noise_median = np.median(edge_data)
    noise_std = np.std(edge_data)

    threshold = noise_median + sigma * noise_std
 
    above_noise = smooth > threshold
    positions = np.where(above_noise)[0]
    # cutoff_freq_low=freq_axis[positions[-1]]
    # cutoff_freq_high=freq_axis[positions[0]]
    # peak_freq=cutoff_freq_high
    # noise = np.std(edge_data)

    if len(positions) > 0:
       return freq_axis[positions[-1]]
