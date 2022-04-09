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

def display_wheels(wheel_selection):
    wheels = get_wheels()[:-1]

    dw = 0 # dw is 'displayed_wheel'
    for increment in range(1, 100, 5):
        wheel = wheels[dw]
        print(wheel)
        time.sleep(0.02 + increment/100)
        os.system(clear_term)
        dw = 0 if dw + 1 >= len(wheels) else dw + 1

def display_welcome_message():