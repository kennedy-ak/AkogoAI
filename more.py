from gtts import gTTS
import os
from playsound import playsound

def text_to_speech_twi(text, output_file):
    # Create gTTS object for Twi language
    tts = gTTS(text=text, lang='tw', slow=False)
    
    # Save the speech to an mp3 file
    tts.save(output_file)
    
    # Play the speech (optional)
    playsound(output_file)

# Example usage
if __name__ == "__main__":
    twi_text = "Afehyia pa"
    output_file = "twi_speech.mp3"
    text_to_speech_twi(twi_text, output_file)
    print(f"Generated and saved Twi speech to {output_file}")
