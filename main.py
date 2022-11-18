import time

import requests
from datetime import datetime
import smtplib

MY_LAT = 5.644553178601829
MY_LONG = -0.06129246103623987

MY_EMAIL = 'tetteynathan89@gmail.com'
MY_PASSWORD = 'zheabtqhplgrjibk'


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    return MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5


def is_night():
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
    return sunset <= time_now.hour or sunrise >= time_now.hour


# If the ISS is close to my current position
# and it is currently dark
while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        # Then send me an email to tell me to look up.
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=['jamesmacgyver442@gmail.com', 'commodorederrick2000@gmail.com'],
                                msg=f'Subject:Look Up\n\n The International Space Station (ISS) is above you in the sky'
                                )
        break



