import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt



def type2(df1, df2, fps_range, row_idx, label_idx, SAVE = False):
    """x axis is resolution, y axis is JOD, color is bitrate"""
    x_values = np.array([1080, 864, 720, 676, 540, 480, 360,]) # resolution

    fig, ax = plt.subplots(figsize=(8, 5))

    for num in range(8, 15): # loop column
        bitrate = df1.iloc[label_idx, 2+7*num]
        print(f'bitrate {bitrate}')

        # cvvdp jod from file1
        jod_cvvdp = df1.iloc[row_idx, 2+7*num:9+7*num].values
        # print(f'jod \n {type(jod)}')
        print(f'jod_cvvdp \n {jod_cvvdp}')

        # marr jod from file2
        jod_marr = df2.iloc[0:7, 1+4*num].values

        print(f'jod_marr \n {jod_marr}')
        jod = jod_cvvdp - jod_marr
        print(f'jod \n {jod}')




        ax.plot(x_values, jod, marker='o', label=bitrate)
        ax.set_xticks(x_values)

    ax.set_xlabel('Resolution')
    ax.set_ylabel('JOD')
    ax.set_title(f'VRR Video Quality')
    ax.grid(True)
    ax.legend()
    if SAVE:
        current_time = datetime.now().strftime("%m%d_%H%M_%S")
        fig.savefig(f"{current_time}.png")
    plt.show()

# Plot cvvdp and marr results from csv files, offset cvvdp values with marr values
# for fixed bandwidth, plot JOD across all fps
if __name__ == "__main__":
    row_idx = 5
    label_idx = 10
    SAVE = False
    LOG = True
    np.set_printoptions(precision=6)

    # file_path1 = 'VRRPlot_0303.xlsx'
    # file_path2 = 'C:/Users/15142/Desktop/VRR/drawVRR_gyorgy/vrr_lookup_0306.xlsx'
    # sheet1_name='0305_notearing' 
    # sheet2_name='Sheet3' 
    file_path1 = 'cvvdp_0312.xlsx'
    file_path2 = 'marr_0312.xlsx'
    sheet1_name='Sheet1' 
    sheet2_name='Sheet1' 
    df1 = pd.read_excel(file_path1, sheet_name=sheet1_name, na_values=['NA'])
    df2 = pd.read_excel(file_path2, sheet_name=sheet2_name, na_values=['NA'])

    # num is number of fps wanted
    fps_range = 8
    type2(df1, df2, fps_range, row_idx, label_idx, SAVE)

