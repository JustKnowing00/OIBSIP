import openmeteo_requests                        #Weather API used here
import pgeocode                                  #for conversion of zip codes to coordinates
import requests_cache                               
from colorama import Fore, init, Style
from datetime import datetime, timedelta         
from retry_requests import retry

time = datetime.now()
date = datetime.now().date()

direction = {                       #for visualization of wind direction
    0 :'↑',
    45 :'↗',
    90 :'→',
    145 :'↘',
    180 :'↓',
    225 :'↙',
    270 :'←',
    315 :'↖'
}

countries = {                       #for converting country names to country codes
    "United States": "US",
    "Canada": "CA",
    "United Kingdom": "GB",
    "Germany": "DE",
    "France": "FR",
    "India": "IN",
    "China": "CN",
    "Japan": "JP",
    "Australia": "AU",
    "Brazil": "BR",
    "South Africa": "ZA",
    "Russia": "RU",
    "Mexico": "MX",
    "Italy": "IT",
    "Spain": "ES",
    "Netherlands": "NL",
    "Saudi Arabia": "SA",
    "South Korea": "KR",
    "Turkey": "TR",
    "Sweden": "SE"
}

timezones = {                       #to assign timezones according to country names
    "United States": "America/New_York",
    "Canada": "America/Toronto",
    "United Kingdom": "Europe/London",
    "Germany": "Europe/Berlin",
    "France": "Europe/Paris",
    "India": "Asia/Kolkata",
    "China": "Asia/Shanghai",
    "Japan": "Asia/Tokyo",
    "Australia": "Australia/Sydney",
    "Brazil": "America/Sao_Paulo",
    "South Africa": "Africa/Johannesburg",
    "Russia": "Europe/Moscow",
    "Mexico": "America/Mexico_City",
    "Italy": "Europe/Rome",
    "Spain": "Europe/Madrid",
    "Netherlands": "Europe/Amsterdam",
    "Saudi Arabia": "Asia/Riyadh",
    "South Korea": "Asia/Seoul",
    "Turkey": "Europe/Istanbul",
    "Sweden": "Europe/Stockholm"
}

country_code = ""
time_zone = ""
direc = ""
country_str = str(input("Enter your Country : "))

for country in countries:
    if country_str.lower() == country.lower():
        country_code = countries[country]
for time_country in timezones:
    if country_str.lower() == time_country.lower():
        time_zone = timezones[time_country]

post_code = str(input("Enter your area zip code : "))
nomi = pgeocode.Nominatim(country_code)
query = nomi.query_postal_code(post_code)

data = {                                              #extracts coordinates
    "lat": query["latitude"],
    "lon": query["longitude"]
}

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)



url = "https://api.open-meteo.com/v1/forecast"
params = {                                              #requests various required data from the API
	"latitude": data["lat"],
	"longitude": data["lon"],
	"current": ["temperature_2m", "relative_humidity_2m", "precipitation", "rain", "surface_pressure", "wind_speed_10m", "wind_direction_10m"],
	"daily": ["temperature_2m_max", "temperature_2m_min", "rain_sum"],
	"timezone": time_zone
}

responses = openmeteo.weather_api(url, params=params)

response = responses[0]

#---------------------------------------------Response Storage for Current Data-------------------------------------
current = response.Current()
current_temperature = current.Variables(0).Value()
current_humidity= current.Variables(1).Value()
current_precipitation = current.Variables(2).Value()
current_rain = current.Variables(3).Value()
current_surface_pressure = current.Variables(4).Value()
current_wind_speed = current.Variables(5).Value()
current_wind_direction= current.Variables(6).Value()

#-------------------------------------------Response Dtorage for Daily Data-----------------------------------------
daily = response.Daily()
daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
daily_rain_sum = daily.Variables(2).ValuesAsNumpy()


#-----------------------------------------Output section----------------------------------------------------------
def visualize_temp(temp, temp_max, temp_min):                       #to visualize temperature in a bar format
    bar = ""
    for i in range(1, 101):
        if i == round(temp):
            bar += "█"
        elif i >= round(temp_min) and i <= round(temp_max):
            bar += "░"
        else:
            bar += "="
    bar += "   █ = Current temperature,  ░ = Temperature variation"
    return bar 

def visualize_temp_btm(temp_max, temp_min):              #assigns values for the bar format
    bar1 = ""
    for i in range(1, 101):
        if i == round(temp_min) - (len(str(round(temp_min))) + 5):
            bar1 += f"{temp_min:.2f}°C┘"
        elif i == round(temp_max) - (len(str(round(temp_min))) + 5):
            bar1 += f"└{temp_max:.2f}°C"
        else:
            bar1 += " "
    return bar1 

def visualize_temp_top(temp):              #assigns values for the bar format
    bar2 = ""
    for i in range(1, 101):
        if i == round(temp):
            bar2 += f"┌{temp:.2f}°C"
        else:
            bar2 += " "
    return bar2

visual_temp = visualize_temp(current_temperature, daily_temperature_2m_max[0], daily_temperature_2m_min[0])
temp_btm = visualize_temp_btm(daily_temperature_2m_max[0], daily_temperature_2m_min[0])
temp_top = visualize_temp_top(current_temperature)

print("\n" + Style.BRIGHT + "---------Location---------" + Style.RESET_ALL)               #Location outpput
print(f"Coordinates : {response.Latitude()}°N {response.Longitude()}°E")
print(f"Timezone : {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Date : {date.strftime("%Y-%m-%d")}")
print(f"Time : {time.strftime("%H:%M:%S")}")

print("\n" + Style.BRIGHT + "----Weather  Condition----" + Style.RESET_ALL)                #Temp, humidity, precipitation and pressure
print("\n              " + temp_top)
print(f"Temperature : {visual_temp}")
print("              " + temp_btm)
print(f"\nHumidity : {current_humidity}%")
print(f"Precipitation : {current_precipitation}mm")
print(f"Pressure : {current_surface_pressure:.3f}Pa")

print("\n" + Style.BRIGHT + "-----------Rain-----------" + Style.RESET_ALL)                #Rainfall output
print(f"\nRainfall today : {current_rain}")
print("Future Estimations : ")
print("   Date    |  Rainfall")
for i in range(1, 7):
    next_day = date + timedelta(days=i)                                                    # Add i days to the current date
    print(str(next_day.strftime("%Y-%m-%d")) + " |    " + str(daily_rain_sum[i]))

print("\n" + Style.BRIGHT + "-----------Wind-----------" + Style.RESET_ALL)                #Wind output
print(f"\nCurrent wind speed : {current_wind_speed:.2f} km/hr")
print(f"Wind Direction : {current_wind_direction:.2f}° ")
print("       N   ")
for x in direction:                                                                       #to get approximate wind direction
    if current_wind_direction >= (x - 22.5) and current_wind_direction < (x + 22.5):
        direc = direction[x]
print(f"    W  {direc}  E")
print("       S   ")