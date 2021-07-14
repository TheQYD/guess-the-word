#!/usr/bin/env python3

import random
import time

import speech_recognition as speech


def recognizeSpeechFromMic(recognizer, microphone):
  
  if not isinstance(recognizer, speech.Recognizer):
    raise TypeError("'recognizer' must be 'Recognizer' instance")

  if not isinstance(microphone, speech.Microphone):
    raise TypeError("'microphone' must be 'Microphone' instance")

  with microphone as source:
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

  response = {
    "success": True,
    "error": None,
    "transcription": None
  }

  try:
    response["transcription"] = recognizer.recognize_google(audio)
    print(response)

  except speech.UnknownValueError:
    response["error"] = "Unable to recognize speech"

  except:
    response["success"] = False
    response["error"] = "API Unavailable"

  return response


if __name__ == "__main__":
  
  words = ["Atlanta", "Pittsburgh", "Chicago", "New York City", "Miami"]
  tries = 3
  prompt_limit = 5

  recognizer = speech.Recognizer()
  microphone = speech.Microphone()

  word = random.choice(words)

  instructions = (
    "I'm thinking of one of these cities: \n"
    "{words}\n"
    "You have {n} tries to guess which one.\n"
  ).format(words=', '.join(words), n=tries)

  print(instructions)

  time.sleep(3)

  for i in range(tries):

    for j in range(prompt_limit):
      print('Guess {}. Speak!'.format(i+1))
      guess = recognizeSpeechFromMic(recognizer, microphone)

      if guess['transcription']:
        break

      if not guess['success']:
        break

      print("I didn't catch that. Could you say that again?\n")

    if guess["error"]:
      print("ERROR: {}".format(guess["error"]))
      break

    print("You said: {}".format(guess['transcription']))

    guess_is_correct = guess["transcription"].lower() == word.lower()
    user_has_more_attempts = i < tries - 1

    if guess_is_correct:
      print("Correct! You win!".format(word))
      break

    elif user_has_more_attempts:
      print("Incorrect. Try again.\n")

    else:
      print("Sorry, you lose!\nI was thinking of '{}'.".format(word))
      break
