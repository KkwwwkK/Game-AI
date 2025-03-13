# Use a pipeline as a high-level helper
from transformers import pipeline
import requests

pipe = pipeline("text2text-generation", model="google/flan-t5-base")

# variables 
guess_words = []
correct_letters = ['@'] * 5
present_letters = set()
absent_letters = set()


# a llm model to generate word, based on a background/prompt
def guess_word(guess_words, correct_letters, present_letters, absent_letters):
    prompt = (
        "Return a five letter word, meet the constraints below,"
    "1, dont use guessed words"
    "2, dont use absent letters"
    "3, try to use present letters in different position when generate the new word"
    "4, use the correct letters at the correct positions"
    "here below is the reference"
    f"guessed words: {"".join(guess_words)}"
    f"correct letters: {"".join(correct_letters)}"
    f"present letters {"".join(present_letters)}"
    f"absent letters: {"".join(absent_letters)}"
    )

    outputs = pipe(prompt, max_new_tokens=len(prompt) + 20)
    word = outputs[0]['generated_text']
    print("here is the : " + word)
    for output in outputs:
        print(f"Result: {output['generated_text']}")
        
    return word
    
# store the guessed words, present letters, absent letters, correct letters
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

# a loop for 6 times of guess, conditional setting for win or lose
def game_start():
    
    max_try = 6
    api_call = "https://wordle.votee.dev:8000/random"
    
    for trial in range(1, max_try + 1):
        guess = guess_word(guess_words, correct_letters, present_letters, absent_letters)
        guess_words.append(guess)
        
        params = {"guess": guess, "size": 5}
        try:
            response = requests.get(api_call, params=params)
            response.raise_for_status
        except requests.RequestException as e:
            print(f"api call failed: {e}")
            break
        
        result = response.json()
        print("show the : " + result)
        
        store_state(guess, result)
        
        if all(letter != "@" for letter in correct_letters):
            print("Bingo!")
    else:
        print("failed!")
        
if __name__ == "__main__":
    game_start()

