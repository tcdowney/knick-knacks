import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches

root_dir = '../temp-data'
save_dir = root_dir + "/graphs"
show_instead_of_save = False
image_extension = '.png'

def plot(csv, plot_title, finish_time):
    csvPath = root_dir + '/' + csv
    data = pd.read_csv(csvPath, header=None, encoding='utf-8', names=['time', 'temp', 'actual_cpu', 'desired_cpu'])
    data['time'] = pd.to_datetime(data['time'])

    start_time_unix_sec = data['time'][0].timestamp()
    data['seconds'] = data['time'].map(lambda x : x.timestamp() - start_time_unix_sec)
    data['actual_cpu'] = data['actual_cpu'].map(lambda x : x / 1000000000)

    sns.set()
    sns.set_style('white')

    ax = sns.lineplot(x='seconds', y='temp', data=data, color='firebrick')
    ax.set(xlabel='Time (Seconds)', ylabel='Temperature (°C)')
    ax.set_title(plot_title)
    ax.set(ylim=(30, 100))

    ax2 = plt.twinx()
    sns.lineplot(x='seconds', y='actual_cpu', data=data, ax=ax2, color='cornflowerblue', alpha=0.35)
    sns.set_style('ticks')

    ax2.set(ylabel='CPU (Ghz)')

    temp_patch = mpatches.Patch(color='firebrick', label='Temp')
    freq_patch = mpatches.Patch(color='cornflowerblue', label='Freq')
    finish_patch = mpatches.Patch(color='black', label='Complete', ls='--', alpha=0.35, hatch='-', fill=False)
    plt.legend(handles=[temp_patch, freq_patch, finish_patch])
    plt.axvline(x=finish_time, color='black', ls='--', alpha=0.35)

    if show_instead_of_save:
        plt.show()
    else:
        save_file = csvPath.replace(root_dir, save_dir).replace('.csv', image_extension)
        plt.gcf().canvas.draw()
        plt.savefig(save_file)
        plt.close()

datasets = [
    ['sysbench-no-heatsink.csv', 'No Heat Sink', 216.8779],
    ['sysbench-with-heatsink.csv', 'Heatsink Only', 181.5579],
    ['sysbench-with-heatsink-fan.csv', 'Heatsink + Fan', 178.6560],
    ['sysbench-with-poe-adapter.csv', 'PoE Adapter', 178.6779],
    ['sysbench-with-argon-neo.csv', 'Argon NEO Case', 178.6092],
    ['sysbench-with-rgb-cooler-tower.csv', 'Cooling Tower', 178.6021],
]

for dataset in datasets:
    plot(dataset[0], dataset[1], dataset[2])
