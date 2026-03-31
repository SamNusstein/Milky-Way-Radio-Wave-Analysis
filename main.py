if __name__ == "__main__":
        import glob
        import re
        import numpy as np
        import pandas as pd
        import Processing.data_Cleaning as data_Cleaning
        import Processing.PeakDetection as PeakDetection
        import matplotlib.pyplot as plt
        import Processing.Plotting as plotting
        import Processing.Calculations as calculations

        c = 299792.458
        f0 = 1420.40575

        path="SkynetFiles"
        data = data_Cleaning.load_data(path, f0, c)
        '''Extract highest velocities above a noise level for each longitude'''
        highest_freq={}
        for col in data.columns[2:]:
            highest_freq[col]=PeakDetection.get_peak_frequency(1.75,data[col].values,col,data['Frequency'].values)

        highest_freq_df=pd.DataFrame(list(highest_freq.items()),columns=['Longitude','Highest_freq'])

        '''This section is for calculations of Mass Radius and Rotation'''

        R, V = calculations.calculate_galactic_rotation(highest_freq_df)

        '''This section is for plotting the results'''
        plotting.spectra_plot(data)
        plotting.plot_rotation_curve(R,V)
        plotting.plot_mass_vs_radius(R, V)