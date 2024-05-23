"""
Cleaning the Snow Depth data:
1. Quality flag
2. Discard unphysical changes in SD
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


meteo = pd.read_csv('Data/Meteo_HEF.dat', header=1, skiprows=[2, 3], parse_dates=['TIMESTAMP'], dtype=np.float64,
                    na_values=["NAN"], index_col='TIMESTAMP')
start = meteo.index[0]
end = meteo.index[-1]
dates = pd.date_range(start, end, freq='10min')
meteo = meteo.reindex(dates)

# Snow Depth (SR50)
SD = meteo.Snow_Depth

# Correct Snow Depth with quality flag from the sensor
SD = SD.where(meteo.Q != 0) #Q = 0 means not able to read distance
SD = SD.where(meteo.Q < 300) # >210 low signal strength; >300 means high uncertainty

# Still some peaks remain after quality flag is applied, that are unreasonable
# Apply scipy find_peaks to find the peaks that are changing more than 0.1m/10min
peaks, _ = find_peaks(SD, threshold=0.1)

SD_corr = SD
SD_corr[peaks] = np.nan

# Scipy only recognizes the positive peaks, to get rid of negative peaks: multiply by -1
peaks2, _ = find_peaks(SD_corr*-1, threshold=0.1)
SD_corr[peaks2] = np.nan

# All values below 0 are also to be discarded
SD_corr = SD_corr.where(SD_corr>=0)




