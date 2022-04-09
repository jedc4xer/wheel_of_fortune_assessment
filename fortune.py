import os
import requests
import time

# Assign system flexible clear variable
clear_term = "cls||clear"
os.system(clear_term)

# Get Wheel Illusions
def get_wheels():
    wheels = requests.get(
        'https://raw.githubusercontent.com/jedc4xer/wheel_of_fortune_assessment/main/ascii_wheels.txt'
    ).text.split(",")
    return wheels

wheels = get_wheels()
for wheel in wheels:
    print(wheel)
    time.sleep(1)
    os.system(clear_term)
