import requests
#this is mostly fawads code, he emailed it to me and I moved stuff around to better suit my needs. I restructured it work as functions
api_key = '3422f67a35069fc75f8e1c755a5a5f4d'

#trying to overwrite, and then rerun

def temp(weather_input):
   weather_data = requests.get(
       f"https://api.openweathermap.org/data/2.5/weather?q={weather_input}&units=imperial&APPID={api_key}")

   if weather_data.json()['cod'] == '404':
       print("No City Found")
   else:
       tempest = round(weather_data.json()['main']['temp'])
       #print(tempest)
       return tempest
   #temp = round(weather_data.json()['main']['temp'])
   #weathererer = weather_data.json()['temp'][0]['main']
   #print(f"The weather in {user_input} is: {weather}")
   #print(f"The temperature in {weather_input} is: {temp}°F")
def weather(weather_input):
   weather_data = requests.get(
       f"https://api.openweathermap.org/data/2.5/weather?q={weather_input}&units=imperial&APPID={api_key}")

   if weather_data.json()['cod'] == '404':
       print("No City Found")
   else:
       weat = weather_data.json()['weather'][0]['main']
       return weat

