import requests
from datetime import datetime
import smtplib
import time

MY_LAT = -36.848461 # Your latitude
MY_LONG = -174.763336 # Your longitude

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

# print(iss_latitude)
# print(iss_longitude)

#Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
current_hour = time_now.hour


#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

lat_difference = MY_LAT - iss_latitude
lon_difference = MY_LONG - iss_longitude
my_email = 'data.micc@gmail.com'
my_password = 'tftlkineiozfxoka'

while True:
    time.sleep(60)
    if (lat_difference >= 5 or lat_difference < -5) and (lon_difference >= 5 or lon_difference < -5) and (current_hour > sunset or current_hour < sunrise):
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg='Subject: ISS is overhead\n\nLook up!'
            )




