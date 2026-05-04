import requests
import time
import sys
from api_comm import upload, transcribe, get_transcription_results

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <audio_file>")
        return

    file_name = sys.argv[1]

    # Upload audio
    audio_url = upload(file_name)

    # Start transcription
    job_id = transcribe(audio_url)

    # Get results
    data, error = get_transcription_results(job_id)

    if data:
        text = data['text']

        # Save to file (optional)
        text_file_name = file_name.rsplit('.', 1)[0] + '.txt'
        with open(text_file_name, 'w') as f:
            f.write(text)

        # 🔥 IMPORTANT: print output for Flask
        print(text)

    else:
        print("ERROR:", error)

if __name__ == "__main__":
    main()