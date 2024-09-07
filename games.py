import random
import requests

# Function to fetch a random word with a length of 6 or fewer letters
def get_random_word():
    try:
        # Fetch a word with DictionaryAPI directly to get both the word and its meaning
        response = requests.get("https://random-word-api.herokuapp.com/word?number=1")
        if response.status_code == 200:
            word = response.json()[0]
            # Check if the word is 6 characters or fewer
            if len(word) <= 5:
                return word
            else:
                return get_random_word()  # Retry if the word is too long
        else:
            print("Error fetching word from the API.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to fetch the definition of a word using the DictionaryAPI
def get_word_definition(word):
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if response.status_code == 200:
            data = response.json()
            definition = data[0]['meanings'][0]['definitions'][0]['definition']
            return definition
        else:
            return "Definition not found."
    except Exception as e:
        return f"An error occurred while fetching the definition: {e}"

def scramble_word(word):
    # Convert the word to a list, shuffle it, and return the scrambled word
    word = list(word)
    random.shuffle(word)
    return ''.join(word)

def play_game():
    while True:
        word = get_random_word()
        if not word:
            print("Could not retrieve a word. Exiting game.")
            return

        scrambled = scramble_word(word)
        definition = get_word_definition(word)
        
        print("Welcome to the Word Scramble Game!")
        print(f"Scrambled word: {scrambled}")
        
        attempts = 3
        while attempts > 0:
            guess = input("Unscramble the word: ").lower()
            if guess == word:
                print(f"Congratulations! The word is '{word}'.")
                print(f"The meaning of the word is: {definition}")
                break
            else:
                attempts -= 1
                print(f"Wrong guess. {attempts} attempts left.")
        
        if attempts == 0:
            print(f"Out of attempts! The word was '{word}'.")
            print(f"The meaning of the word is: {definition}")
        
        replay = input("One more round? (y/n): ").lower()
        if replay != 'y':
            print("Thanks for playing!")
            break

# Start the game
play_game()
