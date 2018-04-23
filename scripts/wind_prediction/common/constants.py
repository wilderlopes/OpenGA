import numpy as np
# Processing raw data
# umed: velocidade média zonal (leste-oeste)
# vmed: velocidade média meridional (norte-sul)

RAWDATAPATH = '../../data/anemometer/rawdata/'
DATASETPATH = '../../data/anemometer/'
FILESHOURLY = ['vmed_meridional.txt', 'umed_zonal.txt', 'dirdom.txt', 'rajh.txt']
FILESDAILY  = ['rajd.txt', 'dirrajd.txt']

# Constants
DATETIME            = 'datetime'
V_AVGSPEED          = 'v_avg_speed'
U_AVGSPEED          = 'u_avg_speed'
MAINDIRECTION       = 'main_direction'
MAINDIRECTIONDEG    = 'main_direction_deg'
MAXGUSTSPEED        = 'max_gust_speed'

# Wind direction: string to float
DIC_WIND_DIRECTION  = {'E':   0.0,
                      'ENE': 22.5,
                      'NE':  45.0,
                      'NNE': 67.5,
                      'N':   90.0,
                      'NNW': 112.5,
                      'NW':  135.0,
                      'WNW': 157.5,
                      'W':   180.0,
                      'WSW': 202.5,
                      'SW':  225.0,
                      'SSW': 247.5,
                      'S':   270.0,
                      'SSE': 292.5,
                      'SE':  315.0,
                      'ESE': 337.5,
                      'C':   np.nan}
