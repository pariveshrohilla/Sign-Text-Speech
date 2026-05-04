import requests
import time
import sys
from api_comm import upload, transcribe, get_transcription_results

def save_transcript(data, error, file_name):
    if data:
        text_file_name = file_name.rsplit('.', 1)[0] + '.txt'
        with open(text_file_name, 'w') as f:
            f.write(data['text'])
        print("Transcription saved to", text_file_name)
    else:
        print("Transcription failed:", error)

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <audio_file>")
        return

    file_name = sys.argv[1]
    
    # Upload the audio file
    audio_url = upload(file_name)
    
    # Start transcription
    job_id = transcribe(audio_url)
    
    # Get transcription results
    data, error = get_transcription_results(job_id)
    
    # Save the transcript
    save_transcript(data, error, file_name)

if __name__ == "__main__":
    main()