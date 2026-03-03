# Requests allows us to make HTTP requests which we will use to get data from an API
from urllib import response

import requests
# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Datetime is a library that allows us to represent dates
import datetime

# Setting this option will print all collumns of a dataframe
pd.set_option('display.max_columns', None)
# Setting this option will print all of the data in a feature
pd.set_option('display.max_colwidth', None)
# Takes the dataset and uses the rocket column to call the API and append the data to the list
def getBoosterVersion(data):
    for x in data['rocket']:
       if x:
        response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
        BoosterVersion.append(response['name'])
        # Takes the dataset and uses the launchpad column to call the API and append the data to the list
def getLaunchSite(data):
    for x in data['launchpad']:
       if x:
         response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
         Longitude.append(response['longitude'])
         Latitude.append(response['latitude'])
         LaunchSite.append(response['name'])
         # Takes the dataset and uses the payloads column to call the API and append the data to the lists
def getPayloadData(data):
    for load in data['payloads']:
       if load:
        response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
        PayloadMass.append(response['mass_kg'])
        Orbit.append(response['orbit'])
        # Takes the dataset and uses the cores column to call the API and append the data to the lists
def getCoreData(data):
    for core in data['cores']:
            if core['core'] != None:
                response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
                Block.append(response['block'])
                ReusedCount.append(response['reuse_count'])
                Serial.append(response['serial'])
            else:
                Block.append(None)
                ReusedCount.append(None)
                Serial.append(None)
            Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
            Flights.append(core['flight'])
            GridFins.append(core['gridfins'])
            Reused.append(core['reused'])
            Legs.append(core['legs'])
            LandingPad.append(core['landpad'])
# 1. Get the data from the API
spacex_url = "https://api.spacexdata.com/v4/launches/past"
response = requests.get(spacex_url)

# 2. Check if the request was successful and convert to JSON
data = pd.json_normalize(response.json())

# 3. Now apply your filtering logic (the code you provided)
data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

# We will remove rows with multiple cores because those are falcon rockets with 2 extra rocket boosters and rows that have multiple payloads in a single rocket.
data = data[data['cores'].map(len)==1]
data = data[data['payloads'].map(len)==1]

# Since payloads and cores are lists of size 1 we will also extract the single value in the list and replace the feature.
data['cores'] = data['cores'].map(lambda x : x[0])
data['payloads'] = data['payloads'].map(lambda x : x[0])

# We also want to convert the date_utc to a datetime datatype and then extracting the date leaving the time
data['date'] = pd.to_datetime(data['date_utc']).dt.date

# Using the date we will restrict the dates of the launches
data = data[data['date'] <= datetime.date(2020, 11, 13)]

BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []

getBoosterVersion(data)
getLaunchSite(data)
getPayloadData(data)
getCoreData(data)

launch_dict = {
    'Booster Version': BoosterVersion,
    'Payload Mass (kg)': PayloadMass,
    'Orbit': Orbit,
    'Launch Site': LaunchSite,
    'Outcome': Outcome,
    'Flights': Flights,
    'Grid Fins': GridFins,
    'Reused': Reused,
    'Legs': Legs,
    'Landing Pad': LandingPad,
    'Block': Block,
    'Reused Count': ReusedCount,
    'Serial': Serial,
    'Longitude': Longitude,
    'Latitude': Latitude
}
df = pd.DataFrame(launch_dict)
print(df.head())

df['Date'] = data['date'].values
df['FlightNumber'] = data['flight_number'].values

# 2. Filter out Falcon 1
# Note: The API returns 'Falcon 1' or 'Falcon 9' in the 'Booster Version' column
# 1. Filter out Falcon 1 to focus only on Falcon 9
# Use 'Booster Version' instead of 'BoosterVersion'
data_falcon9 = df[df['Booster Version'] != 'Falcon 1'].copy()

# 2. Reset FlightNumber
data_falcon9['FlightNumber'] = list(range(1, data_falcon9.shape[0] + 1))

# 3. Calculate mean and replace NaN values
# Use 'Payload Mass (kg)' instead of 'PayloadMass'
mean_payload = data_falcon9['PayloadMass'].mean()
data_falcon9['PayloadMass'] = data_falcon9['PayloadMass'].fillna(mean_payload)

# 4. Verify results
print(data_falcon9.isnull().sum())
print(data_falcon9.head())
# Replace the np.nan values with its mean value
mean_payload = data_falcon9['PayloadMass'].mean()
data_falcon9['PayloadMass'].replace(np.nan, mean_payload, inplace=True) 
# Check launch site counts
print(data_falcon9['Launch Site'].value_counts())

# Check total Falcon 9 count
print(f"Total Falcon 9: {data_falcon9.shape[0]}")

# Check missing Landing Pad values
print(f"Missing Landing Pads: {data_falcon9['Landing Pad'].isnull().sum()}")