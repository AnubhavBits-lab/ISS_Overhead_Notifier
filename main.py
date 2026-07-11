import smtplib
import requests
from datetime import datetime
import os

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("ISS_PASSWORD")
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.
def checkpos():
    diff_lat = abs(MY_LAT - iss_latitude)
    diff_long = abs(MY_LONG - iss_longitude)
    if diff_lat < 5 and diff_long < 5:
        return True
    else:
        return False


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("http://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
print(data)
sunrise_h = int(data["results"]["sunrise"].split("T")[1].split(":")[0])+5
sunset_h = int(data["results"]["sunset"].split("T")[1].split(":")[0])+5
sunrise_m = int(data["results"]["sunrise"].split(":")[1].split(":")[0])
sunset_m = int(data["results"]["sunset"].split(":")[1].split(":")[0])
if sunrise_m>=30:
    sunrise_m = sunrise_m-30
    sunrise_h+=1
else:
    sunrise_m = sunrise_m+30
if sunset_m>=30:
    sunset_m = sunset_m-30
    sunset_h+=1
else:
    sunset_m = sunset_m+30

time_now = datetime.now()

if checkpos():
    if time_now.hour > sunset_h or time_now.hour < sunrise_h:
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs="SEND_EMAIL", msg=f"Look up! ISS is above you :)")

print(iss_latitude, iss_longitude)
