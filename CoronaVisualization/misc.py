
import pandas as pd
from datetime import datetime, timedelta
import datetime as dt
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import pickle


def plot_profiles(profiles, xlab, ylab, labels, interval):

    # plt.figure(num=None, figsize=(20, 10), dpi=300, facecolor='w', edgecolor='k')

    fig, ax = plt.subplots(dpi=300, figsize=(10, 5))

    dts = [dtm.strftime('%H:%M') for dtm in
           datetime_range(datetime(2016, 9, 1, 0), datetime(2016, 9, 2, 0), timedelta(minutes=interval))]
    loc = range(0, len(dts), 10)
    dts_x = [dts[i] for i in loc]


    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown',
              'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan', 'gold', 'lime', 'black',
              'magenta']

    styles = ['-', '--', '-.', ':', '--']
    markers = ['x', 'x', 'v', 's', '*', 'p', '+', 'D', 'v']
    marker_id = 0

    markes_pos = list(range(0, len(profiles[1]), 4))

    for i in range(0, len(profiles)):

        lbl = '.'.join(labels[i].split('_')[1:])

        month = int(lbl.split('.')[-2])

        # if month == 1:
        #     c = (1.0, 0.6, 0.2)
        # elif month == 2:
        #     c = (0.0, 1.0, 0.0)
        # elif month == 3:
        #     c = (0.0, 0.0, 1.0)
        # else:
        #     c = (1.0, 0.0, 0.0)

        marker = None
        if i > len(styles)-1:
            style = '-'
            marker = markers[marker_id]
            marker_id += 1
        else:
            style = styles[i]

        ax.plot(profiles[i], label=lbl, linestyle=style, marker=marker, markevery=markes_pos, lw=2, color=colors[i])

    ax.set_axisbelow(True)
    ax.grid(True)
    plt.xticks(loc, dts_x, rotation='vertical')
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")

    ax.tick_params(labelsize='medium', width=3)

    plt.show()


    # plt.figure(num=None, figsize=(16, 9), dpi=300, facecolor='w', edgecolor='k')
    # dts = [dtm.strftime('%H:%M') for dtm in datetime_range(datetime(2016, 9, 1, 0), datetime(2016, 9, 2, 0), timedelta(minutes=interval))]
    # loc = range(0, len(dts), 10)
    # dts_x = [dts[i] for i in loc]
    #
    # for i in range(0, len(profiles)):
    #     plt.plot(profiles[i], label=labels[i], lw=5)
    #
    # plt.xticks(loc, dts_x, rotation='vertical')
    # plt.xlabel(xlab)
    # plt.ylabel(ylab)
    # plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    #
    #
    #
    # plt.show()


def relative(data, to='max'):

    a = np.array(data)

    if to == 'max':
        b = a.max()
        if np.isnan(b):
            b = get_max(data)
        return a / b * 100

    else:
        to = int(to)
        return a / to * 100



def smooth(data, window_size, poly_order):
    return savgol_filter(data, window_size, poly_order)


def get_max(array):
    max = 0
    for a in array:
        if a > max:
            max = a
    return max


def sigma_filter(times_orig, speeds_orig):
    sig_lower, sig_upper = three_sigma(speeds_orig)

    speeds_filtered = []
    times_filtered = []
    for i in range(0, len(speeds_orig)):
        if speeds_orig[i] < sig_upper:
            speeds_filtered.append(speeds_orig[i])
            times_filtered.append(times_orig[i])

    return np.array(times_filtered), np.array(speeds_filtered)


def three_sigma(x):
    return x.mean() - 3 * x.std(), x.mean() + 3 * x.std()


def IQR(datacolumn, iqr=1.5):
    datacolumn = sorted(datacolumn)
    Q1, Q3 = np.percentile(datacolumn, [25, 75])
    IQR = Q3 - Q1
    lower_range = Q1 - (iqr * IQR)
    upper_range = Q3 + (iqr * IQR)
    return lower_range, upper_range



def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


def addSecs(tm, secs):
    fulldate = datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + timedelta(seconds=secs)
    return fulldate.time()



def get_speed_profile(times, speeds, interval=15):
    dts = [dtm.strftime('%H:%M') for dtm in datetime_range(datetime(2016, 9, 1, 0), datetime(2016, 9, 2, 0), timedelta(minutes=interval))]
    lower = dt.time(0, 0)
    higher = addSecs(lower, interval * 60)

    speed_profile = []

    for i in range(0, len(dts)):

        #current_time = '[' + str(lower) + '-' + str(higher) + ']'
        #print(current_time)

        temp_table = []

        # TODO: Napraviti listu posjecenih indeksa da se ubrza for petlja

        for j in range(0, len(times)):
            time = pd.to_datetime(times[j]).time()
            if lower <= time < higher:
                temp_table.append(speeds[j])

        if len(temp_table) > 0:
            speed_profile.append(np.mean(np.array(temp_table)))
        else:
            speed_profile.append(50)




        # print(speed_profile)


        lower = higher
        higher = addSecs(lower, interval * 60)

    return speed_profile


def save_pickle_data(path, data):
    """
    Saves data in the pickle format.
    :param path: Path to save.
    :param data: Data to save.
    :return:
    """
    try:
        with open(path, 'wb') as handler:
            pickle.dump(data, handler, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)


def open_pickle(path):
    """
    Opens pickle data from defined path.
    :param path: Path to pickle file.
    :return:
    """
    try:
        with open(path, 'rb') as handle:
            data = pickle.load(handle)
            return data
    except Exception as e:
        if hasattr(e, 'message'):
            print(e.message)
            return None
        else:
            print(e)
            return None


