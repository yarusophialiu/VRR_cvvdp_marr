import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

#  [16000 32000  8000  1000  2000  4000   500]
# bandwidth [ 9.680344   10.37349118  8.98719682  6.90775528  7.60090246  8.29404964
#   6.2146081 ]

def type1(df, label_idx, number, refresh_rate, bitrate, SAVE = False):
    """x axis is bandwidth, y axis is JOD, color is resolution"""
    # bandwidth_dict = {10.37349118: 32000, 9.680344: 16000, 8.98719682:8000}
    fig, ax = plt.subplots(figsize=(8, 5))
    # print(f'df type1 \n {df}')

    # print(row_start, row_end)
    # print(f'bitrate \n {repr(bandwidth)}')
    
    # if LOG:
    #     bandwidth = np.log(bandwidth)
    #     print(f'bandwidth {bandwidth}')

    labels = ['1080p', '864p', '720p', '480p', '360p']
    # labels = ['1080p', '864p', '720p', '540p', '480p', '360p']
    # labels = ['1080p', '864p', '720p', '540p', '480p', '360p']
    colors = ['blue', 'greenyellow', 'red', 'green', 'orange',]
    # colors = ['blue', 'greenyellow', 'red', 'gray', 'cyan', 'green', 'orange',]
    # plt.figure(figsize=(8, 5))

    # collect data for each resolution
    # manually skip the resolution we dont want
    resolution_not_want = ['540p']
    for i, resolution in enumerate(labels):
        # print(f'i resolution {i, resolution}')

        if resolution in resolution_not_want:
            continue

        jod = []
        for num in range(0, number): # e.g. first 3 fps, i.e. 30, 60, 70
            # print(f'num {num}')
            # cvvdp jod from file1
            val = df.iloc[label_idx, 2+i+5*num]
            # print(f'index {2+i+5*num}')
            jod.append(val)
            # print(f'val \n {val}')
        ax.plot(refresh_rate, jod, marker='o', label=labels[i], linestyle='-', color=colors[i])
        # print(f'jod {jod}')
# jod = np.delete(jod_cvvdp, 3) # delete value at resolution 676
    # for i in range(2, 9): # loop column
    #     jod = df.iloc[row_start:row_end, i+7*num].values
    #     # print(f'jod \n {jod}')
    #     ax.plot(refresh_rate, jod[sorted_indices], marker='o', label=labels[i-2], linestyle='-', color=colors[i-2])

    ax.set_xlabel('Refresh rate (Hz)')
    ax.set_xticks(refresh_rate)
    # ax.set_xticklabels([30, 60, 70, 75, 80, 85, 90, 120, 150, 160])
    ax.set_ylabel('JOD')
    # ax.set_title(f'VRR Video Quality - fps {30+ 10*num}')
    ax.set_title(f'VRR Video Quality - bitrate {bitrate/1000} Mbps')

    ax.grid(True)
    ax.legend()

    if SAVE:
        current_time = datetime.now().strftime("%m%d_%H%M_%S")
        plt.savefig(f"{current_time}.png")
    plt.show()



def type2(df, label_idx, bitrate, number, labels, SAVE = False):
    """x axis is resolution, y axis is JOD, color is bitrate"""
    # df = pd.read_excel(file_path, sheet_name=n)
    # print(f'df type2 \n {df}')
    # x_values = np.array([1080, 864, 720, 540, 480, 360,]) # resolution
    x_values = np.array([1080, 864, 720, 480, 360,]) # resolution

    fig, ax = plt.subplots(figsize=(8, 5))
    # labels =  [60, 70, 80, 90, 120, 150, 160]
    for num in range(number): # loop column
        # cvvdp jod from file1
        jod_cvvdp = df.iloc[label_idx, 2+5*num:7+5*num].values
        print(f'jod_cvvdp \n {(jod_cvvdp)}')

        # if has 676 column
        # jod = df.iloc[label_idx, 2+7*num:9+7*num].values
        # jod = np.delete(jod_cvvdp, 3) # delete value at resolution 676
        # print(f'jod_cvvdp \n {jod}')
        print(f'num {num}')

        ax.plot(x_values, jod_cvvdp, marker='o', label=f'{labels[num]} fps')
        ax.set_xticks(x_values)

    ax.set_xlabel('Resolution')
    ax.set_ylabel('JOD')
    ax.set_title(f'VRR Video Quality - bitrate {bitrate/1000} Mbps')
    ax.grid(True)
    ax.legend()
    if SAVE:
        current_time = datetime.now().strftime("%m%d_%H%M_%S")
        fig.savefig(f"{current_time}.png")
    plt.show()


# Plot cvvdp results from csv file
# in type 2 change 2+6*num:9+6*num to 2+7*num:9+7*num if has 676 column
if __name__ == "__main__":
    SAVE = True
    LOG = True

    file_path = 'cvvdp_0326.xlsx'
    sheet_name='sunroom_0328' # sunroom_0328
    df = pd.read_excel(file_path, sheet_name=sheet_name, na_values=['NA'])
    # bitrate_dict = {16000: 0, 32000: 1, 8000: 2, 1000: 3, 2000: 4, 4000: 5, 500: 6}
    bitrate_dict = {500: 0, 1000: 1, 2000: 2, 4000: 3, 8000: 4, 16000: 5, 32000: 6}
    refresh_rate = [60, 70, 80, 90, 120, 150, 160]
    bitrates = [4000]
    # num = 10
    # num_of_fps = 10

    for bitrate in bitrates:
        type1(df, bitrate_dict[bitrate], len(refresh_rate), refresh_rate, bitrate, SAVE)
        type2(df, bitrate_dict[bitrate], bitrate, len(refresh_rate), refresh_rate, SAVE)
