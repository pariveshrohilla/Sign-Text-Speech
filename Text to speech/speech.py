from gtts import gTTS
import sys
import os
from datetime import datetime

def main():
    if len(sys.argv) != 3:
        print("ERROR")
        print("ERROR")
        return

    text = sys.argv[1]
    lang = sys.argv[2]

    filename = f"tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"

    # IMPORTANT: DO NOT hardcode path here
    # Just generate audio file in current folder
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

    print(filename)
    print(text)

if __name__ == "__main__":
    main()