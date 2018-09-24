import pandas as pd
import matplotlib.pyplot as plt
import common.constants as constants

# action = 'create'
# action = 'rotors'
action = 'complete'

if action == 'create':

    filename = "../../data/NASA-GRIP/GRIP-MMS/GRIP_MM_20100810_20HZ.txt"
    first_row = 52
    f = open(filename)

    list_rows = []
    for line in f:
        list_rows.append(line)

    # print(len(list_rows))
    # input()
    list_rows = list_rows[first_row:40000]

    for i in range(int(len(list_rows)/2)):
        print(i, int(len(list_rows)/2))

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

    df.to_csv('../../data/NASA-GRIP/GRIP-MMS/NASA_GRIP_MMS_master.csv')

elif action == 'rotors':

    df_master = pd.read_csv('../../data/NASA-GRIP/GRIP-MMS/NASA_GRIP_MMS_master.csv')

    df_master = df_master[constants.COLS_FOR_SIM_ROTORS]
    print(df_master.head())
    df = df_master[10000:16100].reset_index()

    # resample from 20Hz to 5Hz
    df = df.iloc[::4, :]
    df = df.reset_index()
    df = df[constants.COLS_FOR_SIM_ROTORS]
    print(df.head())
    print(df.columns)
    print('len(df) = {}'.format(len(df)))
    input()
    df.to_csv('../../data/NASA-GRIP/GRIP-MMS/NASA_GRIP_MMS_rotors.csv')
    # Plotting
    # pd.scatter_matrix(df[constants.COLS_FOR_SIM])
    fig = plt.figure()
    for col in [df.columns[0]]:
        plt.plot(df.index.values, df[col].values, label=col)
        plt.legend()
    fig = plt.figure()
    for col in df.columns[1:]:
        plt.plot(df.index.values, df[col].values, label=col)
    plt.legend()


    plt.show()

elif action == 'complete':

    df_master = pd.read_csv('../../data/NASA-GRIP/GRIP-MMS/NASA_GRIP_MMS_master.csv')

    df_master = df_master[constants.COLS_FOR_SIM_COMPLETE]
    print(df_master.head())
    df = df_master[10000:].reset_index()

    # resample from 20Hz to 5Hz
    df = df.iloc[::4, :]
    df = df.reset_index()
    df = df[constants.COLS_FOR_SIM_COMPLETE]
    print(df.head())
    print(df.columns)
    print('len(df) = {}'.format(len(df)))
    input()
    df.to_csv('../../data/NASA-GRIP/GRIP-MMS/NASA_GRIP_MMS_complete.csv')
    # Plotting
    # pd.scatter_matrix(df[constants.COLS_FOR_SIM])
    fig = plt.figure()
    for col in [df.columns[0]]:
        plt.plot(df.index.values, df[col].values, label=col)
        plt.legend()
    fig = plt.figure()
    for col in df.columns[1:-1]:
        plt.plot(df.index.values, df[col].values, label=col)
    plt.legend()
    fig = plt.figure()
    for col in [df.columns[-1]]:
        plt.plot(df.index.values, df[col].values, label=col)
    plt.legend()


    plt.show()
