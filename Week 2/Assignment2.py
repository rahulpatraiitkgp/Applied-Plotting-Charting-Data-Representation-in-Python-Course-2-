
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d25/95a36bccd19775da17da3ef1f16841967a571944d768cf29975f87e4.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Kharagpur, West Bengal, India**, and the stations the data comes from are shown on the map below.

# In[1]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(25,'95a36bccd19775da17da3ef1f16841967a571944d768cf29975f87e4')


# In[6]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib notebook')

df1 = pd.read_csv('./data/C2A2_data/BinnedCsvs_d25/95a36bccd19775da17da3ef1f16841967a571944d768cf29975f87e4.csv')

minimum = []
maximum = []
month = []
df1 = df1[~(df1['Date'].str.endswith(r'02-29'))]
times1 = pd.DatetimeIndex(df1['Date'])


df = df1[times1.year != 2015]
times = pd.DatetimeIndex(df['Date'])
for j in df.groupby([times.month, times.day]):
    minimum.append(min(j[1]['Data_Value']))
    maximum.append(max(j[1]['Data_Value']))
    
df2015 = df1[times1.year == 2015]
times2015 = pd.DatetimeIndex(df2015['Date'])
minimum2015 = []
maximum2015 = []
for j in df2015.groupby([times2015.month, times2015.day]):
    minimum2015.append(min(j[1]['Data_Value']))
    maximum2015.append(max(j[1]['Data_Value']))
    
minaxis = []
maxaxis = []
minvals = []
maxvals = []
for i in range(len(minimum)):
    if((minimum[i] - minimum2015[i]) > 0):
        minaxis.append(i)
        minvals.append(minimum2015[i])
    if((maximum[i] - maximum2015[i]) < 0):
        maxaxis.append(i)
        maxvals.append(maximum2015[i])

plt.figure()
colors = ['green', 'red']
plt.plot(minimum, c='green', alpha = 0.5, label = 'Minimum Temperature (2005-14)')
plt.plot(maximum, c ='red', alpha = 0.5, label = 'Maximum Temperature (2005-14)')
plt.scatter(minaxis, minvals, s = 10, c = 'blue', label = 'Record Break Minimum (2015)')
plt.scatter(maxaxis, maxvals, s = 10, c = 'black', label = 'Record Break Maximum (2015)')
plt.gca().fill_between(range(len(minimum)), 
                       minimum, maximum, 
                       facecolor='blue', 
                       alpha=0.25)

plt.ylim(-300, 600)
plt.legend(loc = 8, frameon=False, title='Temperature', fontsize=8)
plt.xticks( np.linspace(15,15 + 30*11 , num = 12), (r'Jan', r'Feb', r'Mar', r'Apr', r'May', r'Jun', r'Jul', r'Aug', r'Sep', r'Oct', r'Nov', r'Dec') )
plt.xlabel('Months')
plt.ylabel('Temperature (tenths of degrees C)')
plt.title(r'Extreme temperature of "Kharagpur, West Bengal, India" by months, with outliers', fontsize=10)
plt.show()


# In[ ]:



