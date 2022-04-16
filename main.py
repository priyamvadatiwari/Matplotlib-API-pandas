

import requests
import json
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timezone
import plotly.graph_objects as go
import openpyxl
import BarChart , Reference 

chart = BarChart ()


#My API Key is c17856fae46dcfdee7fb3ae1a4301558

cities = ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Winnipeg', 'Quebec City',
'Hamilton', 'Kitchener', 'London', 'Victoria', 'Halifax', 'Oshawa', 'Windsor', 'Saskatoon', 'St. Catharines', 'Regina', 'St. Johns', 'Kelowna']


'''Step 2 - Get the data by making API calls.'''

filename = "data.json"

#This code is commented because Data.json file is already created and loaded.This is the live data so it may change.
'''citiesList =[]
for city in cities:
  url1 = f'https://api.openweathermap.org/data/2.5/weather?q={Toronto},CA&appid=c17856fae46dcfdee7fb3ae1a4301558'
  r = requests.get(url1)
  print(f"Statucode: {r.status_code}")
  city_dict = r.json()
  citiesList.append(city_dict)
  
with open(filename, 'w') as jsonFile:
  jsonFile.write(json.dumps(citiesList, indent=3))'''

#read the data from the json file and store it in the obj. This object will be used in all the questions as per the requirement. 
with open(filename) as file_obj:
  cities_weather = json.load(file_obj)

'''
Step 3: Analysis and Visualization
Question1(A):Using Scattergeo, plot the current temperature in the aforementioned cities. The plot
should have:
'''

#Creating empty list to add the date from the obj
citytemperatures,longitudes,latitudes = [],[],[]   

#For loop to read through each temperature, long and lat for location. 
for city_temp in cities_weather:
  tempr = city_temp['main']['temp']
  long = city_temp['coord']['lon']
  lat = city_temp['coord']['lat']
  citytemperatures.append(tempr)
  longitudes.append(long)
  latitudes.append(lat)


# Create the scattergeo plot for temperatures and show them in a map. 
data = [{
  "type": 'scattergeo', 
  "lon":longitudes,
  "lat":latitudes,
  "marker": {
    "size": [0.05*mag for mag in citytemperatures],
    "color":citytemperatures,
    "colorscale":"electric",
    "reversescale":True,
    "colorbar":{"title":"Temperature(Kelvin)"}
    }
}]
my_layout = Layout(title = "Temperature Map")

figure = {'data': data, 'layout': my_layout}
offline.plot(figure, filename = 'temperaturemap.html')   #this will create the temperature map of the 20 cities in Canada.

'''Question 1(B):Using Scattergeo, plot the current humidity in the aforementioned cities.'''

humidities,hum_longs,hum_lats = [],[],[]   
#For loop to read through each humidity, longitude and latitude for locations. 
for city_humid in cities_weather:
  print(city_humid)
  humidity = city_humid['main']['humidity']
  Hlong = city_humid['coord']['lon']
  Hlat = city_humid['coord']['lat']
  humidities.append(humidity)
  hum_longs.append(Hlong)
  hum_lats.append(Hlat)

# Create the scattergeo plot for humidity. 
dataHum = [{
  "type": 'scattergeo', 
  "lon":hum_longs,
  "lat":hum_lats,
  "marker": {
    "size": [0.2*mag for mag in humidities],
    "color":humidities,
    "colorscale":"spectral",
    "reversescale":True,
    "colorbar":{"title":"Humidity Level(%)"}
    }
}]
my_layout2 = Layout(title = "City wise humidity Map")

figure = {'data': dataHum, 'layout': my_layout2}
offline.plot(figure, filename = 'humiditymap.html')   #this will create the humidity map of the 20 cities in Canada.

'''Question 3.1.C: Using Matplotlib, plot a clustered bar chart for temperature and humidity'''

#continuing from the above code, storing both the lists in the dictionary and then create a dataframe.
weather_dict = {
  'temperatures': citytemperatures, 
  'humidities': humidities
  }

#create a dataframe
df = pd.DataFrame(weather_dict, columns=['temperatures','humidities'])
fig = plt.figure() # Create matplotlib figure
ax = fig.add_subplot(111) # Create matplotlib axes
ax2 = ax.twinx() # Create another axes that shares the same x-axis as ax.
width = 0.3
df.temperatures.plot(kind='bar', color='brown', ax=ax, width=width, position=1)
df.humidities.plot(kind='bar', color='green', ax=ax2, width=width, position=0)
ax.set_ylabel('Humidity Level')
ax2.set_ylabel('Temperature(Kelvin)')
plt.title('Humidity vs Temperature')
plt.show()


'''Question 2 : using Plotly, create a bar plot with the count of each weather description.
##For each of the cities, extract the following information:'''

weather_desc = []

for desc in cities_weather:

  description = desc['weather'][0]['description']
  weather_desc.append(description)        #Add all the descriptions to the list

#create a dataframe with the dictionary.
desc_dictionary = {'description': weather_desc}   
desc_df = pd.DataFrame(desc_dictionary, columns = ['description'])
desc_df.drop_duplicates(subset = "description")
desc_df["description"].value_counts(sort= True)

#Create a pivot table and use aggfunc. 
weather_description = desc_df.pivot_table(columns=['description'], aggfunc='size')
#print table
print (weather_description)

#Create the plot to show the weather description and count
fig4 = plt.figure()
ax = fig4.add_subplot(111)
width = 0.5
weather_description.plot(kind = 'bar')

ax.set_ylabel('Weather description')
ax.set_xlabel('Count')
plt.title('Unique Weather description')
plt.show()

'''Question 3: From the given list of cities, extract and print the cities with the most wind speed as
well as the least wind speed. Don’t forget to print out the wind speeds for both of them as well.'''

winds, cities_sp = [],[]
for cityweather in cities_weather:
  wind = cityweather['wind']['speed']
  winds.append(wind)
  
for city in cities_weather:
  city = city['name']
  cities_sp.append(city)

#create a dictionary with speed and city key and assign winds and cities_sp lists as values. 
windsdict = {'speed' : winds,
              'city'  : cities_sp
}

dfwind = pd.DataFrame(windsdict, columns = ['speed', 'city'])
max_ind = dfwind["speed"].idxmax()                  # Index of maximum in column
min_ind = dfwind["speed"].idxmin()                  # Index of minimum in column

print(f"The city with minimum wind speed of {dfwind['speed'].min()} is {dfwind['city'][min_ind]}")
print(f"The city with maximum wind speed of {dfwind['speed'].max()} is {dfwind['city'][max_ind]}")

'''Question 4: for the list of the cities, using data.json, for each city do the following:'''
def avgtime(timestringlist):
  minutecounts = []
  for val in timestringlist:
    h = val[:2]
    m = val[3:5]
    total_minutes = (int(h)*60) + int(m)
    minutecounts.append(total_minutes)
  avgtimemins = sum(minutecounts)/len(minutecounts)
  hours = int(avgtimemins/60)
  minutes = avgtimemins % 60
  return f"{hours} hours and {minutes} minutes"

sunrise, sunset, daylight = [],[],[]
for city in cities_weather:
  sunrise.append(city['sys']['sunrise'])
  sunset.append(city['sys']['sunset'])
  cityname = city['name']
  duration = datetime.utcfromtimestamp(city['sys']['sunset'] - city['sys']['sunrise']).strftime("%H:%M")
  daylight.append(duration)
  print(duration)
  print(f"The duration of light today, in {cityname}, was {duration.split()}")

print(f"The average length of the daylight in all the cities is {avgtime(daylight)}")


'''Question 5: for the each city, using data.json:
1. Extract the actual temperature from the dictionary as well as the feels like temperature
and calculate the difference between those values.
2. Following that, print out the name of the city and the difference between the actual
temperature and feels like values.
Sample output for the city of Yellowknife:'''

for temp in cities_weather:
  acttemp = temp['main']['temp']
  feeltemp = temp['main']['feels_like']
  city = temp['name']
  dif= acttemp - feeltemp
  print(f"The difference between the actual temperature and 'feels like' temperature for {city} is {dif} degrees.")

#I think there is a significant difference in the actual temperatures and 'feels-like' temperatures for some of the cities. It is mainly due to the local weather conditions such as humidity, and wind speed, air temperature."


'''Question 6:
Select any city from the list of cities mentioned above.
2. Using data.json, get the weather data for the city of your choice and store it in a
dictionary.
3. From that dictionary, extract the wind speed.
4. After that, create a gauge chart (https://plotly.com/python/gauge-charts/).'''

#My choice of city is Calgary
city = 'Calgary'
windspeed = {}   #Create an empty dictionary to add windspeeds. 
for speed in cities_weather:
  windspeed[speed['name']]  = speed['wind']['speed']

windspeedval = windspeed[city]

# create the gauge chart:
fig6 = go.Figure(go.Indicator(
  mode  = 'gauge+number',
  value = windspeedval,
  domain = {'x' :[0,1],'y':[0,1]},
  title = {'text': 'Wind Speed for Calgary'}))
offline.plot(fig6, filename = "windspeed.html")

'''**********************End Of Final Project - Python ****************************'''