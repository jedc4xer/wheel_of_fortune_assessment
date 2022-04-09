# wheel_of_fortune_assessment
Repository for holding files relating to the Wheel of Fortune Python Assessment

Goal:
    Make as much money as possible while guessing letters that make up a word or phrase that fall under a 
    specific category. 
    
    Players Make Money by spinning a wheel. 
    Section of wheel that they land on determines how much money is received for each consonant guess.
    
Possible Outcomes:
    1. Wheel lands on a number
        A. Player guesses consonant that is in the puzzle
            Result: They receive money shown on wheel
                (Does not matter how many times consonant appears)
        B. Player guesses a consonant that is not in the puzzle
            Result: Player turn ends, and they receive no money
    2. Wheel lands on BANKRUPT
        Result: Player's turn ends, and they receive no money for that round. 
    3. (STRETCH) Wheel lands on Million dollar segment
            Result: If player completes the round as champion, they get the million dollars
    4. (STRETCH) Player lands on Jackpot
            Result: If player correctly answers the question, they get 5000 + the amount of all wheel spins
            to that point in the round added to their bank.
    5. (STRETCH) Player lands on mystery
            Result: Player randomly receives either 1000 or bankruptcy
            
Rules:
    1. If a player guesses a consonant successfully
        Result: They get to buy a vowel for $250, and can continue to buy vowels.
        You can only buy a vowel with the money earned during that round.
    2. A player can guess the answer at any point on their turn
        Result: If they guess the anwer correctly, they win the round. 
                If they guess the answer wrong, they lose their turn.
    3. The player with the most money at the end of round 2 goes on to round 3
    4. If the answer is guessed, the round is over.
    5. At the beginning of round 3, R-S-T-L-N-E are all revealed. The player can then guess 3 more consonants and 1 more vowel at no cost.
    6. For round 3, they have one opportunity and no more than 5 seconds to guess the correct answer.
    7. The prize for the final round is determined by me.
    
Gameplay:
    1. Spin the wheel
    2. Take action based on wheel selection
    3. Spin wheel for consonants
    
Wheel:
    1. Wheel has 24 segments 24*3 (just change probability for million dollar version).
    2. 4 Segments are bankrupt.
    3. Many segments have cash values in $50 intervals between 100 and 900
    4. One segment is lose a turn
    5. One Segment is jackpot
    6. One Segment is million dollars
    7. One Segment is mystery
    
    Questions:
        is 26 segments okay due to million dollar version?
        there is discrepancy in assessment terminology over whether to use counter or guess for final round.
        Is black okay?