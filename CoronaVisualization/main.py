

import pandas as pd
from misc import get_speed_profile, sigma_filter, relative, smooth, plot_profiles, save_pickle_data, open_pickle
import matplotlib.pyplot as plt

import glob



# data_folder = r'D:\DATA_\radni dani_oborine_mix\2020\Radar'
# #data_folder = r'D:\DATA_\radni dani_oborine_mix\2019\odabrani'
#
# files = glob.glob(data_folder + "\*.csv")
#
# # string = "file_name;speed_profile\n"
#
# profiles = []
# labels = []
#
#
# speeding_count = 0
# n_data = 0
#
# br = 1
# for f in files:
#
#     print("{0}/{1}".format(br, len(files)))
#     br += 1
#
#     file_name = f.split('\\')[-1][0:-4]
#
#     data = pd.read_csv(f, sep=',', engine='c')  #, names=['time', 'speed', 'x', 'length', 'lane', 'direction'])
#     data.timestamp = pd.to_datetime(data.timestamp)
#
#     times_orig = data.timestamp.values
#     speeds_orig = data.speed.values
#
#     n_data += len(speeds_orig)
#
#     for s in speeds_orig:
#         if s > 55:
#             speeding_count += 1
#
#
#
#     times_filtered, speeds_filtered = sigma_filter(times_orig, speeds_orig)
#
#     # speed_profile = get_speed_profile(times_orig, speeds_orig, 15)
#     speed_profile = get_speed_profile(times_filtered, speeds_filtered, 15)
#
#     # relative_sp = list(relative(speed_profile, '50'))
#
#     s_smooth = smooth(speed_profile, 13, 3)
#     #s_smooth = speed_profile
#
#     profiles.append(s_smooth)
#     labels.append(file_name)
#
#     # string_profile = ','.join(map(str, s_smooth))
#     # string += file_name + ";" + string_profile + "\n"
#
#
# save_pickle_data('profiles.pkl', profiles)
# save_pickle_data('labels.pkl', labels)

profiles = open_pickle('profiles.pkl')
labels = open_pickle('labels.pkl')

plot_profiles(profiles, 'Time', 'Speed (km/h)', labels, 15)



# f = open("sped_profiles_filtered_smooth_2019.csv", "w")
# f.write(string)
# f.close()

# print('N_DATA: {0}'.format(n_data))
# print('N_SPEEDING: {0}'.format(speeding_count))
# print('PERCENTAGE_SPEEDING: {0}%'.format(round(speeding_count/n_data*100, 2)))

#speed_profile = open_pickle('sp.pkl')
#relative_sp = open_pickle('r_sp.pkl')

#s_smooth = smooth(speed_profile, 13, 3)
#r_smooth = smooth(relative_sp, 13, 3)









