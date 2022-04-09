import os
import requests
import time
import string

# Assign system flexible clear variable
clear_term = "cls||clear"
os.system(clear_term)

def get_files(path):
    file = requests.get(path).text
    return file

def get_wheels():
    path = 'https://raw.githubusercontent.com/jedc4xer/wheel_of_fortune_assessment/main/ascii_wheels.txt'
    wheels = get_files(path).split(",")
    return wheels

def get_template():
    path = 'https://raw.githubusercontent.com/jedc4xer/wheel_of_fortune_assessment/main/template.txt'
    template = get_files(path).split(",")
    return template

def get_words(difficulty):
    path = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
    words = get_files(path).replace("\n", "").split("\r")
    
    if difficulty == 'easy':
        word_subset = [_ for _ in words if (len(_) <= 7 and len(_) > 5)]
    elif difficulty == 'medium':
        word_subset = [_ for _ in words if (len(_) <= 12 and len(_) > 7)]
    elif difficulty == 'hard':
        word_subset = [_ for _ in words if (len(_) <= 18 and len(_) > 12)]
    elif difficulty == 'basic assessment':
        word_subset = [
            _ for _ in words if (
            len(_) > 18 and 
            _.count('a') <= 2 and 
            _.count('e') <= 2
            )]
    total = "{:,}".format(len(words))
    filtered = "{:,}".format(len(word_subset))
    print(f'{total} words found - Filtering to {filtered} words\n\n')
    return word_subset
        
def display_wheels(wheel_selection):
    wheels = get_wheels()[:-1]

    dw = 0 # dw is 'displayed_wheel'
    for increment in range(1, 100, 5):
        os.system(clear_term)
        wheel = wheels[dw]
        print(wheel)
        time.sleep(0.02 + increment/100)  
        dw = 0 if dw + 1 >= len(wheels) else dw + 1

def display_welcome_message():
    template = get_template()
    
    # Display a flashing welcome message
    sleep_duration = 2
    for inc in range(20):
        os.system(clear_term)
        if inc > 1:
            sleep_duration = 0.2
            print(template[(inc % 2) + 1])
        else:
            print(template[0])
        time.sleep(sleep_duration)
    print(template[2])

def check_input(input_str,type_requirement,limits):
    
    # If the input requires a name
    if type_requirement == 'name':
        cleaned = [_ for _ in input_str if (_ == " " or _.isalpha())]
        if (len(input_str) == len(cleaned) and len(input_str) <= limits):
            return True
    print(f'{input_str} is not a valid {type_requirement}.')
    time.sleep(2)
    return False

def display_players(players, detail):
    if detail == 'name':
        print("\n",' ** PLAYER NAMES **')
        for assigned in players.keys():
            assigned_name = players[assigned]['name']
            if assigned_name == None:
                print(f'  {assigned}: [empty]')
            else:
                print(f'  {assigned}: {assigned_name}')
        print("\n")
    elif detail == 'full':
        print("\n",' ** PLAYER INFORMATION **')
        for assigned in players.keys():
            print(players[assigned])
    elif detail == 'dash':
        print("\n",' ** PLAYER INFORMATION **')
        for assigned in players.keys():
            name = players[assigned]['name']
            bank = players[assigned]['bank']
            stash = players[assigned]['stash']
            print(f' {assigned}: {name} | Bank: ${bank} | Round Stash: ${stash}')
        print('\n')
            
def set_difficulty():
    passed = False
    while not passed:
        difficulty = input("  Game Difficulty: >> ")
        passed = check_input(difficulty,'number',4)
def get_players():
    
    players = {
        'Player 1': {
            'name': None, 'bank': 0, 'stash': 0, 'guesses': 0, 'correct': 0
        }, 
        'Player 2': {
            'name': None, 'bank': 0, 'stash': 0, 'guesses': 0, 'correct': 0
        }, 
        'Player 3': {
            'name': None, 'bank': 0, 'stash': 0, 'guesses': 0, 'correct': 0
        }
    }
    
    # User Name Input Loop
    passed = 0
    while passed < 3:
        for player in players.keys():
            display_players(players,'name')
            if players[player]['name'] == None:
                player_name = input(f"  Please enter the name of {player}: >> ").strip()
                valid_name = check_input(player_name,'name',50)
                if valid_name:
                    players[player]['name'] = player_name.upper()
                    passed += 1
            os.system(clear_term)
    return players
                    
#def round_controller(players, current_round):
 #   if current_round < 3:
        
#display_welcome_message()

#players = get_players()
#display_players(players,'dash')
words = get_words('medium')