import pandas as pd
import matplotlib.pyplot as plt
import common.constants as constants

filename = "../../data/NASA-GRIP/GRIP-MMS/GRIP_MM_20100810_20HZ.txt"
first_row = 52
f = open(filename)

list_rows = []
for line in f:
    list_rows.append(line)

list_rows = list_rows[first_row:1002]

for i in range(int(len(list_rows)/2)):
    # print(i, len(list_rows))
    string_row = list_rows[2*i][:-1] + list_rows[2*i+1][:-1]
    string_row = string_row.split()

    if i==0:
        columns = string_row
        df = pd.DataFrame(columns=columns)
    else:
        string_row = [[float(x)] for x in string_row]
        row = pd.DataFrame(data=dict(zip(columns, string_row)))
        df = df.append(row)

df.reset_index(inplace=True)
# df.drop(['Unnamed: 0'], axis=1, inplace=True)
# print(df.columns)
print(df[constants.COLS_FOR_SIM])

df[constants.COLS_FOR_SIM].to_csv('../../data/NASA-GRIP/GRIP-MMS/NASA_GRIP_MMS.csv')

# Plotting
# pd.scatter_matrix(df[constants.COLS_FOR_SIM])
#
# fig = plt.figure()
# plt.plot(df.index.values, df[constants.PITCH].values, color='green', label=constants.PITCH)
# plt.plot(df.index.values, df[constants.ROLL].values, color='b', label=constants.ROLL)
# plt.plot(df.index.values, df[constants.YAW].values, color='red', label=constants.YAW)
# plt.legend()
#
# fig = plt.figure()
# plt.plot(df.index.values, df[constants.MACHNUMBER].values, color='green', label=constants.MACHNUMBER)
#
# plt.show()
