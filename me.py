import requests
import pygame
import time
import speech_recognition as sr

# Define the API endpoint and subscription key
url = "https://translation-api.ghananlp.org/tts/v1/tts"
subscription_key = "ac22989547f04e979df0b7e89beed41b"

# Function to play audio file
def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)

# # Function to convert text to speech using Ghana NLP API
# def text_to_speech(text, language):
#     headers = {
#         "Content-Type": "application/json",
#         "Cache-Control": "no-cache",
#         "Ocp-Apim-Subscription-Key": subscription_key
#     }
#     payload = {
#         "text": text,
#         "language": language
#     }
#     response = requests.post(url, headers=headers, json=payload)
#     if response.status_code == 200:
#         audio_file = "output_audio.wav"
#         with open(audio_file, "wb") as f:
#             f.write(response.content)
#         print(f"Audio file saved as '{audio_file}'")
#         play_audio(audio_file)
#     else:
#         print(f"Error: {response.status_code}")
#         print(response.text)

# Function to recognize speech using speech_recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    recognized_text = recognize_speech()
    if recognized_text:
        text_to_speech(recognized_text, "tw")
