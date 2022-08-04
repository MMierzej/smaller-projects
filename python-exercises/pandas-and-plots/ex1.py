import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import datetime


def intify(d): return int(d.replace(' ', ''))


infections = pd.read_csv("https://arcgis.com/sharing/rest/content/items/b03b454aed9b4154ba50df4ba9e1143b/data?",
                         delimiter=';', encoding='windows-1250', converters={'Nowe przypadki': intify})
infections.to_csv('infections2020.csv')
temperatures = pd.read_csv('avg_temps.csv', delimiter=',', encoding='utf-8')


# conversions to datetime.date
infections['Date'] = infections['Data'].apply(
    lambda data: datetime.datetime.strptime(data, '%d.%m.%Y').date())
temperatures['Date'] = temperatures['Date'].apply(
    lambda data: datetime.datetime.strptime(data, '%Y-%m-%d').date())

# setting time boundaries
first_date = max(temperatures['Date'].iloc[0], infections['Date'].iloc[0])
last_date = min(temperatures['Date'].iloc[-1], infections['Date'].iloc[-1])
sep2020 = datetime.date(2020, 9, 1)
may2020 = datetime.date(2020, 5, 1)

# unifying the time frames
infections_trim = infections.loc[(first_date <= infections['Date']) & (
    infections['Date'] <= last_date)]
temperatures_trim = temperatures.loc[(first_date <= temperatures['Date']) & (
    temperatures['Date'] <= last_date)]

# slicing data into periods of interest
inf_nonwave = infections_trim.loc[(may2020 <= infections_trim['Date']) & (
    infections_trim['Date'] <= sep2020)]
tem_nonwave = temperatures_trim.loc[(may2020 <= temperatures_trim['Date']) & (
    temperatures_trim['Date'] <= sep2020)]
inf_wave = infections_trim.loc[sep2020 <= infections_trim['Date']]
tem_wave = temperatures_trim.loc[sep2020 <= temperatures_trim['Date']]

# drawing 2 subplots
fig, axs = plt.subplots(2)
fig.suptitle('2020')  # data are from 2020

for ax in axs:
    ax.grid(True)
    ax.xaxis.set_major_formatter(
        mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))

# B part
axs[0].set_ylabel('Temperature', color='tab:red')
axs[0].plot(tem_nonwave['Date'],
            tem_nonwave['Temperature'], color='tab:red')

# two y-axes, because the two plotted datasets are of different magnitudes
axs01 = axs[0].twinx()

axs01.set_ylabel('New cases', color='tab:blue')
axs01.plot(inf_nonwave['Date'],
           inf_nonwave['Nowe przypadki'], color='tab:blue')

# on the above subplot it can be observed that in August 2020
# infections in fact did rise substantially, despite August being
# a relatively very warm month
# this suggest that waves can begin even during warm seasons


# A part
axs[1].set_ylabel('Temperature', color='tab:red')
axs[1].plot(tem_wave['Date'],
            tem_wave['Temperature'], color='tab:red')

axs11 = axs[1].twinx()

axs11.set_ylabel('New cases', color='tab:blue')
axs11.plot(inf_wave['Date'],
           inf_wave['Nowe przypadki'], color='tab:blue')

# on the above subplot it can be observed
# that there exists a following correlation of data:
# daily infection numbers rise with the fall of daily temperature
# in the plotted months of 2020

plt.show()
