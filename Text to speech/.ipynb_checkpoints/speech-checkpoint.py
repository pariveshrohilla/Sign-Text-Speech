from gtts import gTTS
import os


# Text to convert to speech
text = "hello world this is a test of gtts library in python for text to speech conversion and audio file generation and playback" 

# Convert text to speech
tts = gTTS(text=text, lang='en', slow=False)

# Save the audio file
tts.save("output.mp3")
print("Audio saved as output.mp3")


from playsound import playsound
playsound("output.mp3")

