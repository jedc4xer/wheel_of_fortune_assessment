import os
import requests
import time
import string
import random
from collections import Counter

# Assign system flexible clear variable
clear_term = "cls||clear"

# Collection for User Params
user_params = []

# Runtime Functions
##################################################


def quick_exit():
    print("\n\n  Taking the walk of shame I see! Was it too difficult?")
    time.sleep(1)
    print(
        "  Couldn't handle the shame and realizing that this moment will go down in history?"
    )
    time.sleep(1)
    print("\n  Here is a consolation prize.")
    time.sleep(0.3)
    print("   ** Hands player paper bag with pretzel and cracker samples **")
    time.sleep(1)
    print("\n  The exit is over there... \n")
    raise SystemExit


# Pause Function
def pause_run(duration):
    if "*" not in user_params:
        time.sleep(duration)


def clean_screen():
    os.system(clear_term)


clean_screen()

# Get Functions
##################################################


def get_files(path):
    return requests.get(path).text


def get_wheels():
    path = "https://raw.githubusercontent.com/jedc4xer/wheel_of_fortune_assessment/main/ascii_wheels.txt"
    # path = "https://raw.githubusercontent.com/jedc4xer/wheel_of_fortune_assessment/main/alternate_wheel.txt"
    wheels = get_files(path).split(",")
    return wheels


def get_template():
    path = "https://raw.githubusercontent.com/jedc4xer/wheel_of_fortune_assessment/main/template.txt"
    template = get_files(path).split(",")
    return template


def get_menus():
    path = "https://raw.githubusercontent.com/jedc4xer/wheel_of_fortune_assessment/main/menus.txt"
    menus = get_files(path).split(",")
    return menus


def get_random_word(words):
    return random.choice(words)


def get_spin_result(layout):
    result = random.choice(layout)
    if result == ("BANKRUPT", "ONE MILLION DOLLARS", "BANKRUPT"):
        result = random.choice(result)
    elif result == "MYSTERY":
        result = random.choice(["MYSTERY BANKRUPT", "MYSTERY 1000"])
    return result


def get_words(difficulty):
    path = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
    words = get_files(path).replace("\n", "").strip().split("\r")

    if difficulty == "easy":
        word_subset = [_ for _ in words if (len(_) <= 7 and len(_) > 5)]
    elif difficulty == "medium":
        word_subset = [_ for _ in words if (len(_) <= 12 and len(_) > 7)]
    elif difficulty == "hard":
        word_subset = [_ for _ in words if (len(_) <= 18 and len(_) > 12)]
    elif difficulty == "basic assessment":
        word_subset = [
            _
            for _ in words
            if (
                len(_) > 18
                and _.count("a") <= 2
                and _.count("e") <= 2
                and _.count("s") <= 1
            )
        ]
    total = "{:,}".format(len(words))
    filtered = "{:,}".format(len(word_subset))
    print(f"  {total} words found - Filtering to {filtered} words\n\n")
    return word_subset


def get_players():

    players = {
        "Player 1": {
            "name": None,
            "bank": 0,
            "stash": 0,
            "guesses": 0,
            "correct": 0,
            "status": None,
            "jackpot": 0,
        },
        "Player 2": {
            "name": None,
            "bank": 0,
            "stash": 0,
            "guesses": 0,
            "correct": 0,
            "status": None,
            "jackpot": 0,
        },
        "Player 3": {
            "name": None,
            "bank": 0,
            "stash": 0,
            "guesses": 0,
            "correct": 0,
            "status": None,
            "jackpot": 0,
        },
    }

    clean_screen()

    # User Name Input Loop
    passed = 0
    while passed < 3:
        for player in players.keys():
            print(template[3])
            print("  ** GAME SETUP **  ".center(78, " "))
            display_players(players, "name")
            if players[player]["name"] == None:
                player_name = input(f"  Please enter the name of {player}: >> ").strip()
                valid_name = check_input(player_name, "name", 50)
                if valid_name:
                    players[player]["name"] = player_name.upper()
                    players[player]["status"] = "Available"
                    passed += 1
            clean_screen()
    print(template[3])
    print("  ** GAME SETUP **  ".center(78, " "))
    display_players(players, "name")
    pause_run(2)
    return players


# This function determines who is eliminated from the game.
def get_final_player(players):

    player_status = []
    for player in players.keys():
        earnings = players[player]["bank"]
        player_status.append((player, earnings))

    maximum = max([_[1] for _ in player_status])
    for item in player_status:
        if item[1] == maximum:
            return item[0]


# Display Functions
##################################################


def wheel_flash(wheel, segment):
    segment = str(segment)
    clean_screen()
    print(wheel)
    print(segment.center(78, " "))


def display_turn_info(player, current_round):
    """ This function displays the active turn information. """
    name = player["name"]
    stash = player["stash"]
    bank = player["bank"]
    print(f"  Current Round: {current_round}\n")
    print(f"  Player Name: {name}\n  Round Stash: ${stash}\n  Total Bank: ${bank}")


def display_possible_earnings(spin):
    if str(spin).isnumeric():
        print(f'  Possible Earnings: ${"{:,}".format(spin)}')
    else:
        print(f"  Possible Earnings: {spin}")


def display_final_stats(players):
    for player in players:
        name = players[player]["name"]
        guesses = players[player]["guesses"]
        correct = players[player]["correct"]
        bank = "{:,}".format(players[player]["bank"])
        accuracy = 0
        if guesses != 0:
            accuracy = round((correct / guesses) * 100, 2)
        print(
            f"{player}: {name}\n  Bank: ${bank}\n  Guesses: {guesses}\n  Correct: {correct}\n  Accuracy: {accuracy}%\n"
        )


def display_wheels(spin, layout):

    dw = 0  # dw is 'displayed_wheel'
    layout_increment = 0
    displayed_layout = [_ for _ in layout[1:]]
    displayed_layout += ["BANKRUPT", "ONE MILLION DOLLARS", "BANKRUPT"]
    displayed_layout *= 20
    for increment in range(1, 510, 10):
        wheel = wheels[dw]
        if increment > 450:
            segment = "???? WHAT IS IT GOING TO BE ????"
        else:
            segment = displayed_layout[layout_increment]
        wheel_flash(wheel, segment)
        time.sleep(0.01 + increment / 500)
        dw = 0 if dw + 1 >= len(wheels) else dw + 1
        layout_increment += 1
    if spin == "MYSTERY 1000" or spin == "MYSTERY BANKRUPT":
        segment = "MYSTERY"
    else:
        segment = spin

    if segment == "MYSTERY":
        print("REVEALING THE MYSTERY".center(78, " "))
        time.sleep(2)
        wheel_flash(wheel, spin)
    else:
        wheel_flash(wheel, segment)
    time.sleep(2)


# Display a flashy welcome message
def display_welcome_message():
    sleep_duration = 2
    for inc in range(20):
        clean_screen()
        if inc > 1:
            sleep_duration = 0.2
            print(template[(inc % 2) + 1])
        else:
            print(template[0])
        time.sleep(sleep_duration)
    clean_screen()
    print(template[2])


def display_players(players, detail):
    if detail == "name":
        print("\n", " ** PLAYER NAMES **")
        for assigned in players.keys():
            assigned_name = players[assigned]["name"]
            if assigned_name == None:
                print(f"  {assigned}: [empty]")
            else:
                print(f"  {assigned}: {assigned_name}")
        print("\n")
    elif detail == "full":
        print("\n", " ** PLAYER INFORMATION **")
        for assigned in players.keys():
            print(players[assigned])
    elif detail == "dash":
        print("\n", " ** PLAYER INFORMATION **")
        for assigned in players.keys():
            name = players[assigned]["name"]
            bank = players[assigned]["bank"]
            stash = players[assigned]["stash"]
            print(f" {assigned}: {name} | Bank: ${bank} | Round Stash: ${stash}")
        print("\n")


def display_word(word, guessed_letters, new_guess, sudden):
    """ This function displays the word and populates it with any new guesses. """
    if not sudden:
        pre_reveal = ""
        for char in word:
            if char in new_guess:
                pre_reveal += "# "
            elif char in string.punctuation:
                pre_reveal += char + " "
            elif char in guessed_letters:
                pre_reveal += char + " "
            else:
                pre_reveal += "_ "

        guessed_letters += new_guess

        # Slow the reveal
        revealing = ""
        for char in pre_reveal:
            clean_screen()
            print(template[3])
            revealing += char
            print(revealing.center(78, " "))
            pause_run(0.1)

        pause_run(2)

    revealed = "  "
    for char in word:
        if char in guessed_letters:
            revealed += char + " "
        elif char in string.punctuation:
            revealed += char + " "
        else:
            revealed += "_" + " "
    clean_screen()
    print(template[3])
    print(revealed.center(78, " "))
    print("")
    guess_status = f"  {len(''.join(_ for _ in word if _ in guessed_letters))} out of {len(word)} characters guessed."
    print(guess_status)
    print("  Used Letters: ", ", ".join(list(set(guessed_letters))), "\n")
    if "*" in user_params:
        print(f"  Word: {word} - CHEAT MODE ACTIVATED ")


# Input Validity Checks
##################################################


def check_input(input_str, type_requirement, limits):

    # This block of logic is checking general gameplay inputs.
    if type_requirement in ["name", "word"]:
        cleaned = [_ for _ in input_str if (_ == " " or _.isalpha())]
        if len(input_str) == len(cleaned) and len(input_str) <= limits:
            return True
    elif type_requirement == "number":
        if input_str.isnumeric():
            if int(input_str) in range(limits + 1):
                return True

    # This block of logic is specifically for checking the input of guesses.
    elif type(type_requirement) == list:
        vowels = ["A", "E", "I", "O", "U"]
        consonants = [_ for _ in string.ascii_uppercase if _ not in vowels]
        cleaned = "".join(_.upper() for _ in input_str if _.isalpha())

        if len(input_str) == len(cleaned) and len(input_str) <= limits:
            input_str = cleaned
            if type_requirement == ["word", "consonant"]:
                if len(input_str) == 1:
                    if input_str in consonants:
                        return True
                else:
                    return True
            elif type_requirement == ["word", "vowel"]:
                if len(input_str) == 1:
                    if input_str in vowels:
                        return True
                else:
                    return True
            elif type_requirement == ["consonant", "vowel"]:
                if (
                    len("".join(_ for _ in input_str if _ in vowels)) <= 1
                    and len("".join(_ for _ in input_str if _ in consonants)) <= 3
                ):
                    return True
                else:
                    type_requirements = "collection of letters as specified"

    print(f"\n  {input_str} is not a valid {type_requirement}.")
    time.sleep(2)
    return False


# Builder Functions
##################################################


def build_player_queue(play):
    player_queue = [
        play.pop(random.randint(0, len(play) - 1)),
        play.pop(random.randint(0, len(play) - 1)),
        play.pop(random.randint(0, len(play) - 1)),
    ]
    return player_queue


def establish_wheel_layout(current_round):
    money_prizes = [_ for _ in range(100, 950, 50)]
    # spare = [random.randrange(1000,5000,500)] # Option removed due to rubric
    # spare = [500, 900] if current_round == 1 else [500, "JACKPOT"]
    spare = [500, 900]  # Removed JACKPOT option due to confusion about rules
    money_prizes += spare
    millions = ("BANKRUPT", "ONE MILLION DOLLARS", "BANKRUPT")
    layout = [
        millions,'AVAILABLE','AVAILABLE','AVAILABLE','AVAILABLE','AVAILABLE',
        'AVAILABLE','AVAILABLE','MYSTERY','AVAILABLE','AVAILABLE','AVAILABLE',
        'BANKRUPT','AVAILABLE','AVAILABLE','AVAILABLE','BANKRUPT','AVAILABLE',
        'AVAILABLE','AVAILABLE','AVAILABLE','LOSE A TURN','AVAILABLE','AVAILABLE'
    ]
    layout = [
        money_prizes.pop(random.randint(0, len(money_prizes) - 1))
        if _ == "AVAILABLE"
        else _
        for _ in layout
    ]
    return layout


# General Gameplay Functions
##################################################


def test_spinner(layout):
    results = []
    for spin in range(100000):
        results.append(get_spin_result(layout))
    summary = dict(Counter(results))
    summary = [
        "  " + str(key) + ": " + str(round((summary[key] / 100000) * 100, 2)) + "%"
        for key in summary.keys()
    ]
    summary.sort(key=lambda x: x.split(": ")[1], reverse=False)
    summary = "\n".join(summary)
    print(f"\n\n  Spin Results: (100,000 spins)\n  ----------------->\n{summary}\n")


# This function allows the user to adjust the difficulty of the game.
def set_difficulty():
    print(menus[0])
    passed = False
    while not passed:
        difficulty = input("  Game Difficulty: >> ")

        if "*" in difficulty:
            user_params.append("*")
            difficulty = difficulty.replace("*", "")
            print("\n  Special Param 1 Set")
            if "^" not in difficulty:
                print("  (You can activate a second cheat code by also entering a ^ when indicating difficulty.)")
                time.sleep(1)
            time.sleep(1)
            

        if "^" in difficulty:
            user_params.append("^")
            difficulty = difficulty.replace("^", "")
            print("\n  Special Param 2 Set")
            time.sleep(1)

        passed = check_input(difficulty, "number", 4)
    difficulty = {"1": "basic assessment", "2": "easy", "3": "medium", "4": "hard"}[
        difficulty
    ]
    return difficulty


def manage_bank(players, player, task, earnings):
    """ This function contols the monetary transactions. """

    if task == "BANKRUPT":
        players[player]["stash"] = 0
    elif task == "WON ROUND":
        players[player]["stash"] += earnings
        players[player]["bank"] += players[player]["stash"]
        players[player]["stash"] = 0
    elif task == "GOOD CONS":
        players[player]["stash"] += earnings
    elif task == "VOWEL":
        players[player]["stash"] -= earnings
    return players


# Heavy Functions (Round Controller, Player Turn, Word Guess)
##################################################


def take_guess(word, guessed_letters, allowed):
    """ This function validates and manages a player guess. """

    passed = False
    while not passed:
        if allowed == ["word", "vowel"]:
            print('\n  You have the opportunity to "Buy a Vowel" for $250.')
        elif "end turn" in allowed:
            print("\n  You do not have enough money to buy a vowel.")
            print('  To end your turn, type "end turn".')
        elif "final round" in allowed:
            print("  You have 5 seconds to guess a word.")
            print('\n  To end your turn, type "end turn".')
            timer_start = time.perf_counter()
        if allowed == ["consonant", "vowel"]:
            print_str = "  Input your guess of up to 3 consonants and 1 vowel: >> "
        else:
            print_str = f"  Guess the {allowed[0]} or {allowed[1]}: >> "
        player_guess = input(f"{print_str}")
        if player_guess.lower() == "end turn":
            return "TURN ENDED"

        if "final round" in allowed:
            allowed = allowed.pop(0)
            duration = time.perf_counter() - timer_start
            if duration > 5:
                print(
                    f"\n  Oh no!!! You took {round(duration - 5,4)} seconds too long."
                )
                return "TURN ENDED"

        if allowed == ["word", "end turn"]:
            allowed = "word"
        passed = check_input(player_guess, allowed, 100)
        if not passed and allowed == "word":
            allowed = ["word", "end turn"]

    # If the allowed inputs are not the group of 3 consonants and 1 vowel.
    player_guess = player_guess.upper()
    attempted_word = False
    if allowed != ["consonant", "vowel"]:
        if len(player_guess) > 1:
            attempted_word = True
            if player_guess == word:
                turn_result = "WON ROUND"
            else:
                turn_result = "BAD GUESS"
                player_guess = []
        else:
            if allowed == ["word", "consonant"]:
                if player_guess in word:
                    turn_result = "GOOD CONS GUESS"
                else:
                    turn_result = "BAD GUESS"
            else:
                if player_guess in word:
                    turn_result = "GOOD VOW GUESS"
                else:
                    turn_result = "BAD VOW GUESS"
    else:
        turn_result = "FREE GUESSES"

    display_word(word, guessed_letters, player_guess, False)

    correct_guesses = 0
    total_guesses = 0
    if not attempted_word:
        for letter in player_guess:
            guessed_letters.append(letter)
            if letter in word:
                correct_guesses += 1
            total_guesses += 1
        word_check = len("".join(_ for _ in word if _ in guessed_letters))
        if word_check == len(word):
            turn_result = "WON ROUND"
    else:
        if turn_result == "WON ROUND":
            correct_guesses = 1
        total_guesses = 1

    # List of variables being sent to parent function.
    return_list = [correct_guesses, total_guesses, guessed_letters, turn_result]

    return return_list


def player_turn(
    players, player, current_round, word, layout, guessed_letters, final_prize
):
    """ This function contains all the actions for each player turn. """

    if current_round < 3:
        spun = False
    else:
        spun = True
        spin = final_prize

    outer_passed = False
    while not outer_passed:
        if spun:
            menu_to_display = menus[2]
        else:
            menu_to_display = menus[1]

        display_word(word, guessed_letters, [], True)
        if current_round == 3:
            display_possible_earnings(spin)

        display_turn_info(players[player], current_round)
        print(menu_to_display)

        num_options = 3
        passed = False
        while not passed:
            choice = input("  Choose an action: >> ")
            passed = check_input(choice, "number", num_options)

        if choice == "1":
            if not spun:
                spin = get_spin_result(layout)
                if "^" not in user_params:
                    display_wheels(spin, layout)

                if spin == "MYSTERY 1000":
                    spin = 1000
                elif spin == "ONE MILLION DOLLARS":
                    spin = 1000000

                display_word(word, guessed_letters, [], True)

                display_possible_earnings(spin)

            display_turn_info(players[player], current_round)

            if not spun:
                current_spin = True
            else:
                current_spin = False
                if current_round < 3:
                    spin = 0
            spun = True

            if spin in ["BANKRUPT", "LOSE A TURN", "MYSTERY BANKRUPT"]:
                if spin == "BANKRUPT":
                    players = manage_bank(players, player, "BANKRUPT", None)
                return players
            else:
                if spun and not current_spin:
                    if players[player]["stash"] < 250:
                        allowed = ["word", "end turn"]
                    else:
                        allowed = ["word", "vowel"]
                else:
                    allowed = ["word", "consonant"]

                if current_round > 2:
                    allowed = ["consonant", "vowel"]

                # This call accepts and analyzes the guess
                guess_result = take_guess(word, guessed_letters, allowed)
                if type(guess_result) != list:
                    return players

                players[player]["correct"] += guess_result[0]
                players[player]["guesses"] += guess_result[1]

                if current_round > 2:
                    if guess_result[3] != "WON ROUND":
                        allowed = ["word", "final round"]
                        guess_result = take_guess(word, guessed_letters, allowed)
                        if type(guess_result) != list:
                            return players
                        players[player]["correct"] += guess_result[0]
                        players[player]["guesses"] += guess_result[1]

                if guess_result in ["TURN ENDED", "LOST TURN"]:
                    return players

                if guess_result[3] == "WON ROUND":
                    if str(spin).isnumeric():
                        earned = spin
                    else:
                        earned = None
                    players = manage_bank(players, player, "WON ROUND", earned)
                    return players
                elif guess_result[3] == "GOOD CONS GUESS":
                    if str(spin).isnumeric():
                        players = manage_bank(players, player, "GOOD CONS", spin)
                elif guess_result[3] == "BAD GUESS":
                    players = manage_bank(players, player, "BANKRUPT", None)
                    return players
                elif guess_result[3] in ["GOOD VOW GUESS", "BAD VOW GUESS"]:
                    players = manage_bank(players, player, "VOWEL", 250)
                    if guess_result[3] == "BAD VOW GUESS":
                        return players

            display_turn_info(players[player], current_round)

        elif choice == "2":
            if spun:
                return players
            else:
                print("  The results will be viewable for 10 seconds.")
                time.sleep(2)
                test_spinner(layout)
                time.sleep(10)
        else:
            quick_exit()


def round_controller(players, current_round):
    word = get_random_word(words).upper()
    guessed_letters = []
    layout = establish_wheel_layout(current_round)
    display_word(word, guessed_letters, [], False)

    available_players = [_ for _ in players.keys()]
    player_queue = build_player_queue(available_players) * 50

    if current_round > 2:
        guessed_letters = ["R", "S", "T", "L", "N", "E"]
        final_prize = random.randrange(10000, 100000, 5000)
        player_queue = [get_final_player(players)]
        for player in players.keys():
            if player not in player_queue:
                print(f" ** {players[player]['name']} Eliminated ** ".center(78, " "))
                print("")
                pause_run(1)
    else:
        final_prize = None

    for player in player_queue:
        starting_bank = players[player]["bank"]
        players = player_turn(
            players, player, current_round, word, layout, guessed_letters, final_prize
        )
        if players[player]["bank"] == starting_bank:
            if current_round > 2:
                print(f"\n  Oops! At least you got ${starting_bank}")
                print("\n\n   The correct word was...\n\n")
                print(word.center(78, " "))
                print("")

                display_final_stats(players)
            else:
                print("\n  Next Player...")
        else:
            print("\n  ***** WE HAVE A WINNER!!!! ***** \n")
            print("  Starting Next Round...\n" if current_round < 3 else "")
            # Update all players banks.
            for player in players.keys():
                players[player]["bank"] += players[player]["stash"]
                players[player]["stash"] = 0
            time.sleep(2)
            if current_round == 3:
                display_final_stats(players)
            return players
        time.sleep(3)


# Build
template = get_template()
menus = get_menus()
display_welcome_message()
wheels = get_wheels()[:-1]

# Prepare
difficulty = set_difficulty()
words = get_words(difficulty)
players = get_players()

#
display_players(players, "dash")

for round_ in [1, 2, 3]:
    round_controller(players, round_)
