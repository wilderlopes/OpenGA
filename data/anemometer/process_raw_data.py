import pandas as pd
import common.constants as constants

# This file pre-processes the raw data and creates Pandas dataframes
# that can be used to do the analysis. You only need to run this if you
# do not have the files dataset_hourly.csv and dataset_daily.csv.

print('Generating datasets to be saved in {}'.format(constants.DATASETPATH))

data = pd.DataFrame()
for filename in constants.FILESHOURLY:
    df = pd.read_csv(constants.RAWDATAPATH + filename)
    df.rename(columns={'data':constants.DATETIME}, inplace=True)
    df.set_index(constants.DATETIME, inplace=True)
    data = pd.concat([data, df], axis=1)

data.rename(columns={'vmed':constants.V_AVGSPEED, 'umed':constants.U_AVGSPEED, 'dirdom':constants.MAINDIRECTION, 'rajh':constants.MAXGUSTSPEED}, inplace=True)
data.to_csv(constants.DATASETPATH + 'dataset_hourly.csv')
print(data.head())
del data

data = pd.DataFrame()
for filename in constants.FILESDAILY:
    df = pd.read_csv(constants.RAWDATAPATH + filename)
    df.rename(columns={'data':constants.DATETIME}, inplace=True)
    df.set_index(constants.DATETIME, inplace=True)
    data = pd.concat([data, df], axis=1)

data.rename(columns={'rajd':constants.MAXGUSTSPEED, 'dirrajd':constants.MAINDIRECTION}, inplace=True)
data.to_csv(constants.DATASETPATH + 'dataset_daily.csv')
print(data.head())
del data
