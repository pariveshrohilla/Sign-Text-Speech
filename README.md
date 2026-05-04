## Sign Language

Sign language is a visual means of communication that uses hand gestures, facial expressions, and body movements instead of spoken words. It is widely used by Deaf and hard-of-hearing communities around the world.

Each sign language has its own grammar and structure. For example, American Sign Language (ASL) and Indian Sign Language (ISL) are distinct languages with unique vocabularies and rules.

Sign language plays a vital role in promoting accessibility and inclusion, enabling effective communication between Deaf and hearing individuals.

[![GitHub stars](https://img.shields.io/github/stars/pariveshrohilla/Sign-Text-Speech?style=social)](https://github.com/pariveshrohilla/Sign-Text-Speech)
[![GitHub forks](https://img.shields.io/github/forks/pariveshrohilla/Sign-Text-Speech?style=social)](https://github.com/pariveshrohilla/Sign-Text-Speech)
[![License](https://img.shields.io/github/license/pariveshrohilla/Sign-Text-Speech)](LICENSE)

**Sign-Text-Speech** converts **text ↔ speech ↔ sign language** for accessibility.

##  Features
-  Text-to-Speech (TTS)
-  Speech-to-Text (STT) 
-  Text-to-Sign Language animations
-  Real-time translation
-  Multi-language support
-  Modern UI

##  Tech Stack
Backend: Python Flask <br>
TTS: gTTS <br>
STT: Speech Recognition <br>
Sign: MediaPipe + OpenCV <br>

## Target Audience
Deaf and Hard-of-Hearing Individuals
Healthcare and Service Providers
Students and Learners
Customer service representatives (banks, retail, hospitality)
Emergency responders (police, firefighters, paramedics)




## Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation

```bash
git clone https://github.com/pariveshrohilla/Sign-Text-Speech.git
```

 Usage
Text To Speech: Type → "Speak"
Speech To Text: Put your pre recorded audio and it converts it into text
Text → Sign: Type → "Generate Sign"

#Modules

Each file is a separate module except the "sign text speech" which integrated all of them together into one in a web page . 

## Text to speech
If you want to run this , open a Untitled.py and put your text in there and it will give you your speech. 

## Speech To Text
If you want to run this , open command terminal for the current file path and run 
```
 python main.py <audiofile name>
```
## Sign Final
It contains the final code to run if u wish to run it seprately ,  open cmd in dedicated terminal and run 
```
python app.py
```
wait for a few seconds and a screen will open where you can see  a blue box and if u show signs , there inside it will give you output below . 


## sign text speech
If you want to run this , same as earlier run cmd and run python sts.py which will give you a link to open in your browser . 
Here you can use all the previous modules together . 
<img width="512" height="180" alt="unnamed" src="https://github.com/user-attachments/assets/ac0126c1-efb0-4f99-bf30-8997bbc77bc6" />
<img width="465" height="583" alt="unnamed" src="https://github.com/user-attachments/assets/f691b649-a597-4201-a74f-229ef97cd41c" />
While training , we fetch these hand points for each frame and then train the model on these points
<img width="300" height="300" alt="unnamed" src="https://github.com/user-attachments/assets/8a6861e0-64a7-4210-ba11-bbd8f039ce0d"/> 
<img width="300" height="250" alt="Screenshot 2026-04-25 000254" src="https://github.com/user-attachments/assets/7d8b89fb-0c4d-4467-800b-d15df807cf18" />







Acknowledgments : 
Google TTS,
MediaPipe , 
SpeechRecognition , 

Made with ❤️ by Parivesh Rohilla
