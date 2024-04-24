import os
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt



def type1(df, label_idx, number, refresh_rate, bitrate, SAVE = False):
    """x axis is bandwidth, y axis is JOD, color is resolution"""
    # bandwidth_dict = {10.37349118: 32000, 9.680344: 16000, 8.98719682:8000}
    fig, ax = plt.subplots(figsize=(8, 5))

    labels = ['1080p', '864p', '720p', '480p', '360p']
    colors = ['blue', 'greenyellow', 'red', 'green', 'orange',]
    # colors = ['blue', 'greenyellow', 'red', 'gray', 'cyan', 'green', 'orange',]

    # collect data for each resolution
    # manually skip the resolution we dont want
    resolution_not_want = ['540p']
    for i, resolution in enumerate(labels):
        # print(f'i resolution {i, resolution}')
        if resolution in resolution_not_want:
            continue

        jod = []
        for num in range(0, number): # e.g. first 3 fps, i.e. 30, 60, 70
            val = df.iloc[label_idx, 2+i+5*num]
            jod.append(val)
            # print(f'val \n {val}')
        ax.plot(refresh_rate, jod, marker='o', label=labels[i], linestyle='-', color=colors[i])

    ax.set_xlabel('Refresh rate (Hz)')
    ax.set_xticks(refresh_rate)
    ax.set_ylabel('JOD')
    ax.set_title(f'VRR Video Quality - bitrate {bitrate/1000} Mbps')
    ax.grid(True)
    ax.legend()

    if SAVE:
        date = datetime.now().strftime("%m%d")
        os.makedirs(date, exist_ok=True)
        current_time = datetime.now().strftime("%m%d_%H%M_%S")
        plt.savefig(f"{date}/{current_time}.png")
    plt.show()
# if i == len(labels) - 1:
#     ax.plot(refresh_rate, jod, marker='o', label=labels[i], linestyle='-', color=colors[i])
#     ax.text(x[-1], y[-1], f'sample {i}')


def type2(df, label_idx, bitrate, number, refresh_rate, SAVE = False):
    """x axis is resolution, y axis is JOD, color is bitrate, labels are refresh rate"""
    x_values = np.array([1080, 864, 720, 480, 360,]) # resolution

    fig, ax = plt.subplots(figsize=(8, 5))
    for num in range(number): # loop column
        # cvvdp jod from file1
        jod_cvvdp = df.iloc[label_idx, 2+5*num:7+5*num].values
        print(f'idx {num}, fps{refresh_rate[num]}, JOD {jod_cvvdp[::-1]}')

        ax.plot(x_values, jod_cvvdp, marker='o', label=f'{refresh_rate[num]} fps')
        ax.set_xticks(x_values)

    ax.set_xlabel('Resolution')
    ax.set_ylabel('JOD')
    ax.set_title(f'VRR Video Quality - bitrate {bitrate/1000} Mbps')
    ax.grid(True)
    ax.legend()
    if SAVE:
        date = datetime.now().strftime("%m%d")
        os.makedirs(date, exist_ok=True)
        current_time = datetime.now().strftime("%m%d_%H%M_%S")
        fig.savefig(f"{date}/{current_time}.png")
    plt.show()


# suitable for cvvdp_0417,  with 30-120fps
# Plot cvvdp results from csv file
# in type 2 change 2+6*num:9+6*num to 2+7*num:9+7*num if has 676 column
if __name__ == "__main__":
    SAVE = True
    LOG = True

    file_path = 'cvvdp_0417.xlsx'
    sheet_name='bistro'
    df = pd.read_excel(file_path, sheet_name=sheet_name, na_values=['NA'])
    # bitrate_dict = {16000: 0, 32000: 1, 8000: 2, 1000: 3, 2000: 4, 4000: 5, 500: 6}
    bitrate_dict = {500: 0, 1000: 1, 2000: 2, 4000: 3, 8000: 4, 16000: 5, 32000: 6}
    refresh_rate = [60, 70, 80, 90, 100, 110, 120,]
    # refresh_rate = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120]

    bitrates = [16000]
    # num = 10
    # num_of_fps = 10

    for bitrate in bitrates:
        type1(df, bitrate_dict[bitrate], len(refresh_rate), refresh_rate, bitrate, SAVE)
        type2(df, bitrate_dict[bitrate], bitrate, len(refresh_rate), refresh_rate, SAVE)
