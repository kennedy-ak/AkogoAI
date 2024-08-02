# import requests

# # Define the API endpoint and subscription key
# url = "https://translation-api.ghananlp.org/tts/v1/tts"
# subscription_key = "ac22989547f04e979df0b7e89beed41b"

# # Define the headers
# headers = {
#     "Content-Type": "application/json",
#     "Cache-Control": "no-cache",
#     "Ocp-Apim-Subscription-Key": subscription_key
# }

# # Define the payload
# payload = {
#     "text": "Ɛte sɛn?",
#     "language": "tw"
# }

# # Send the POST request
# response = requests.post(url, headers=headers, json=payload)

# # Check the response
# if response.status_code == 200:
#     # Save the audio file
#     with open("output_audio.wav", "wb") as f:
#         f.write(response.content)
#     print("Audio file saved as 'output_audio.wav'")
# else:
#     print(f"Error: {response.status_code}")
#     print(response.text)


import requests
import pygame
import time

# Define the API endpoint and subscription key
url = "https://translation-api.ghananlp.org/tts/v1/tts"
subscription_key = "ac22989547f04e979df0b7e89beed41b"

# Define the headers
headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
    "Ocp-Apim-Subscription-Key": subscription_key
}

# Define the payload
payload = {
    "text": "Ɛte sɛn?",
    "language": "tw"
}

# Send the POST request
response = requests.post(url, headers=headers, json=payload)

# Check the response
if response.status_code == 200:
    # Save the audio file
    audio_file = "output_audio.wav"
    with open(audio_file, "wb") as f:
        f.write(response.content)
    print(f"Audio file saved as '{audio_file}'")

    # Initialize Pygame mixer
    pygame.mixer.init()
    
    # Load and play the audio file
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    
    # Wait for the audio file to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(1)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
