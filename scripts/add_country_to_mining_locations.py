import pandas as pd
from geopy.geocoders import Nominatim
import time

df = pd.read_csv('data/mining_locations.csv')

geolocator = Nominatim(user_agent="geoapiExercises")

def get_country(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), language='en')
        if location and 'country' in location.raw['address']:
            return location.raw['address']['country']
    except:
        return None

df['country'] = None

for idx, row in df.iterrows():
    country = get_country(row['lat'], row['lon'])
    df.at[idx, 'country'] = country
    time.sleep(1)  # API 호출 제한 방지를 위해 딜레이

df.to_csv('data/mining_locations_with_country.csv', index=False)
