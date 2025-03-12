# # Use a pipeline as a high-level helper
# from transformers import pipeline
# import requests



# pipe = pipeline("text2text-generation", model="google/flan-t5-base")


# # variables 
# guess_words = []
# correct_letters = ['@'] * 5
# present_letters = set()
# absent_letters = set()


# import re

# def guess_word(guess_words, correct_letters, present_letters, absent_letters):
#     prompt = (
#         "Generate a valid five-letter word that follows these constraints:\n"
#         "1. The word must have exactly 5 letters.\n"
#         "2. Do not use any words from this list: " + ", ".join(guess_words) + "\n"
#         "3. Do not include these letters anywhere: " + ", ".join(absent_letters) + "\n"
#         "4. Use these letters, but in a different position: " + ", ".join(present_letters) + "\n"
#         "5. The word must include these letters in the correct positions: " + "".join(correct_letters) + "\n"
#         "Only return a single five-letter word as output."
#     )

#     outputs = pipe(prompt, max_new_tokens=10)  # Reduce token count to avoid long words
#     word = outputs[0]['generated_text'].strip().lower()

#     # Extract only five-letter words using regex
#     match = re.search(r'\b[a-zA-Z]{5}\b', word)
#     if match:
#         word = match.group(0)
#     else:
#         print("LLM generated an invalid word, retrying...")
#         return guess_word(guess_words, correct_letters, present_letters, absent_letters)  # Retry with the same constraints

#     print("Generated word:", word)
#     return word

# # # a llm model to generate word, based on a background/prompt
# # def guess_word(guess_words, correct_letters, present_letters, absent_letters):
# #     prompt = (
# #         "Return a five letter word, meet the constraints below,"
# #     "1, dont use guessed words"
# #     "2, dont use absent letters"
# #     "3, try to use present letters in different position when generate the new word"
# #     "4, use the correct letters at the correct positions"
# #     "here below is the reference"
# #     f"guessed words: {"".join(guess_words)}"
# #     f"correct letters: {"".join(correct_letters)}"
# #     f"present letters {"".join(present_letters)}"
# #     f"absent letters: {"".join(absent_letters)}"
# #     )

# #     outputs = pipe(prompt, max_new_tokens=len(prompt) + 20)
# #     word = outputs[0]['generated_text']
# #     print("here is the : " + word)
# #     for output in outputs:
# #         print(f"Result: {output['generated_text']}")
        
# #     return word
    
# # store the guessed words, present letters, absent letters, correct letters
# def store_state(word, response):
#     global correct_letters, present_letters, absent_letters
    
#     for i, res in enumerate(response):
#         letter = word[i]
#         if res['result'] == 'correct':
#             correct_letters[i] = letter
#         elif res['result'] == 'present':
#             present_letters.add(letter)
#         elif res['result'] == 'absent':
#             if letter not in correct_letters and letter not in present_letters:
#                 absent_letters.add(letter) 

# # a loop for 6 times of guess, conditional setting for win or lose
# def game_start():
    
#     max_try = 6
#     api_call = "https://wordle.votee.dev:8000/random"
    
#     for trial in range(1, max_try + 1):
#         guess = guess_word(guess_words, correct_letters, present_letters, absent_letters)
#         guess_words.append(guess)
        
#         params = {"guess": guess, "size": 5}
#         try:
#             response = requests.get(api_call, params=params)
#             response.raise_for_status
#         except requests.RequestException as e:
#             print(f"api call failed: {e}")
#             break
        
#         result = response.json()
#         print("show the : " + result)
        
#         store_state(guess, result)
        
#         if all(letter != "@" for letter in correct_letters):
#             print("Bingo!")
#     else:
#         print("failed!")
        
# if __name__ == "__main__":
#     game_start()

from transformers import pipeline
import requests
import random
import re

# Load a list of valid five-letter words (You can replace this with a larger list)
VALID_WORDS = ["apple", "grape", "brick", "flame", "spike", "sugar", "table", "pride", "sword", "cloud"]

pipe = pipeline("text2text-generation", model="google/flan-t5-base")

# Variables
guess_words = []
correct_letters = ['@'] * 5
present_letters = set()
absent_letters = set()

def guess_word(guess_words, correct_letters, present_letters, absent_letters):
    prompt = (
        "Generate a single valid five-letter English word that meets these constraints:\n"
        "1. The word must be exactly 5 letters long.\n"
        "2. Do not use any words from this list: " + ", ".join(guess_words) + "\n"
        "3. Do not include these letters anywhere: " + ", ".join(absent_letters) + "\n"
        "4. Use these letters, but in a different position: " + ", ".join(present_letters) + "\n"
        "5. The word must include these letters in the correct positions: " + "".join(correct_letters) + "\n"
        "Only return a single five-letter word with no extra text."
    )

    outputs = pipe(prompt, max_new_tokens=10)
    word = outputs[0]['generated_text'].strip().lower()

    # Extract only valid five-letter words
    match = re.search(r'\b[a-z]{5}\b', word)
    if match and word in VALID_WORDS:
        word = match.group(0)
        print("Generated valid word:", word)
        return word
    else:
        print("LLM generated an invalid word, selecting randomly...")
        return random.choice([w for w in VALID_WORDS if w not in guess_words])  # Pick a valid word

# Store the guessed words, present letters, absent letters, and correct letters
def store_state(word, response):
    global correct_letters, present_letters, absent_letters
    
    for i, res in enumerate(response):
        letter = word[i]
        if res['result'] == 'correct':
            correct_letters[i] = letter
        elif res['result'] == 'present':
            present_letters.add(letter)
        elif res['result'] == 'absent':
            if letter not in correct_letters and letter not in present_letters:
                absent_letters.add(letter) 

# A loop for 6 guesses with win/lose conditions
def game_start():
    max_try = 6
    api_call = "https://wordle.votee.dev:8000/random"

    for trial in range(1, max_try + 1):
        guess = guess_word(guess_words, correct_letters, present_letters, absent_letters)
        guess_words.append(guess)

        params = {"guess": guess, "size": 5}
        try:
            response = requests.get(api_call, params=params)
            response.raise_for_status()
            result = response.json()
        except requests.RequestException as e:
            print(f"API call failed: {e}")
            break

        print("API response:", result)
        store_state(guess, result)

        if all(letter != "@" for letter in correct_letters):
            print("Bingo! You found the word!")
            return

    print("Failed! The word was not found.")

if __name__ == "__main__":
    game_start()


