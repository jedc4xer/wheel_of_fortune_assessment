import os
import requests
import time
import string
import random

# Assign system flexible clear variable
clear_term = "cls||clear"
os.system(clear_term)

def get_files(path):
    return(requests.get(path).text)

def get_wheels():
    path = 'https://raw.githubusercontent.com/jedc4xer/wheel_of_fortune_assessment/main/ascii_wheels.txt'
    wheels = get_files(path).split(",")
    return wheels

def get_template():
    path = 'https://raw.githubusercontent.com/jedc4xer/wheel_of_fortune_assessment/main/template.txt'
    template = get_files(path).split(",")
    return template

def get_menus():
    path = 'https://raw.githubusercontent.com/jedc4xer/wheel_of_fortune_assessment/main/menus.txt'
    menus = get_files(path).split(",")
    return menus

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
            _.count('e') <= 2 and 
            _.count('s') <= 1
            )]
    total = "{:,}".format(len(words))
    filtered = "{:,}".format(len(word_subset))
    print(f'  {total} words found - Filtering to {filtered} words\n\n')
    return word_subset

def get_random_word(words):
    return(random.choice(words))

def display_word(word, guessed_letters, new_guess):
    
    pre_reveal = ""
    for char in word:
        if char in new_guess:
            pre_reveal += "# "
        elif char in string.punctuation:
            pre_reveal += char + " "
        elif char in guessed_letters:
            pre_reveal += char + " "
        else:
            pre_reveal += '_ '
    
    guessed_letters += new_guess
 
    # Slow the reveal
    revealing = ""
    for char in pre_reveal:
        os.system(clear_term)
        print(template[3])
        revealing += char
        print(revealing.center(78," "))
        time.sleep(0.2)
        
    time.sleep(2)
    
    revealed = "  "
    for char in word:
        if char in guessed_letters:
            revealed += char + " "
        elif char in string.punctuation:
            revealed += char + " "
        else:
            revealed += "_" + " "
    os.system(clear_term)
    print(template[3])
    print(revealed.center(78," "))
        
#     guess_status = f"  |  {len(''.join(_ for _ in random_word if _ in guesses))} out of {len(random_word)} characters guessed."
#     print("\n    ", display_string, guess_status)
        
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
    elif type_requirement == 'number':
        if input_str.isnumeric():
            if int(input_str) in range(limits + 1):
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
        
def display_turn_info(player,current_round):
    """ This function displays the active turn information. """
    name = player['name']
    stash = player['stash']
    bank = player['bank']
    print(f"  Current Round: {current_round}\n")
    print(f"  Player Name: {name}\n  Round Stash: ${stash}\n  Total Bank: ${bank}")
    
    
            
def set_difficulty():
    print(menus[0])
    passed = False
    while not passed:
        difficulty = input("  Game Difficulty: >> ")
        passed = check_input(difficulty,'number',4)
    difficulty = {'1':'basic assessment', '2':'easy','3':'medium','4':'hard'}[difficulty]
    return difficulty

def get_players():
    
    players = {
        'Player 1': {
            'name': None,
            'bank': 0,
            'stash': 0,
            'guesses': 0,
            'correct': 0,
            'status': None
        }, 
        'Player 2': {
            'name': None,
            'bank': 0,
            'stash': 0,
            'guesses': 0,
            'correct': 0,
            'status': None
        }, 
        'Player 3': {
            'name': None,
            'bank': 0,
            'stash': 0,
            'guesses': 0,
            'correct': 0,
            'status': None
        }
    }
    
    os.system(clear_term)
    
    # User Name Input Loop
    passed = 0
    while passed < 3:
        for player in players.keys():
            print(template[3])
            print("  ** GAME SETUP **  ".center(78," "))
            display_players(players,'name')
            if players[player]['name'] == None:
                player_name = input(f"  Please enter the name of {player}: >> ").strip()
                valid_name = check_input(player_name,'name',50)
                if valid_name:
                    players[player]['name'] = player_name.upper()
                    players[player]['status'] = 'Available'
                    passed += 1
            os.system(clear_term)
    return players

def establish_wheel_layout():
    money_prizes = [_ for _ in range(100,950,50)]
    spare = [random.randrange(1000,5000,500)]
    money_prizes += spare
    millions = ('BANKRUPT','ONE MILLION DOLLARS','BANKRUPT')
    layout = [
        millions,'AVAILABLE','AVAILABLE','AVAILABLE','JACKPOT','AVAILABLE',
        'AVAILABLE','AVAILABLE','MYSTERY','AVAILABLE','AVAILABLE','AVAILABLE',
        'BANKRUPT','AVAILABLE','AVAILABLE','AVAILABLE','BANKRUPT','AVAILABLE',
        'AVAILABLE','AVAILABLE','AVAILABLE','LOSE A TURN','AVAILABLE','AVAILABLE'
    ]
    layout = [
        money_prizes.pop(random.randint(0,len(money_prizes)-1)) 
        if _ == 'AVAILABLE' else _ for _ in layout
    ]
    return layout

def get_spin_result(layout):
    result = random.choice(layout)
    if result == ('BANKRUPT','ONE MILLION DOLLARS','BANKRUPT'):  
        result = random.choice(result)
    return result

def test_spinner(layout):
    results = []
    for spin in range(100000):
        results.append(get_spin_result(layout))
    summary = dict(Counter(results))
    summary = ["  " + str(key) + ": " + str(round((summary[key]/100000) * 100,2)) + "%" for key in summary.keys()]
    summary.sort(key = lambda x: x.split(": ")[1], reverse = False)
    summary = "\n".join(summary)
    print(f'\n\n  Spin Results: (100,000 spins)\n  ----------------->\n{summary}\n')
    

def build_player_queue(play):
    player_queue = [
        play.pop(random.randint(0,len(play)-1)),
        play.pop(random.randint(0,len(play)-1)),
        play.pop(random.randint(0,len(play)-1))
    ]
    return player_queue

def player_turn(players,player,current_round,word):
    """ This function contains all the actions for each player turn. """
    print(template[3])
    display_turn_info(players[player],current_round)
    print(menus[1])
    
    
def round_controller(players, current_round):
    word = get_random_word(words).upper()
    layout = establish_wheel_layout()
    display_word(word, [_ for _ in word], ['A'])
    if current_round < 3:
        available_players = [_ for _ in players.keys()]
        player_queue = build_player_queue(available_players)
        for player in player_queue:
            player_turn(players,player,current_round,word)
            
            
            

template = get_template()
menus = get_menus()        
#display_welcome_message()

difficulty = set_difficulty()
words = get_words(difficulty)

players = get_players()
display_players(players,'dash')


round_controller(players,1)
