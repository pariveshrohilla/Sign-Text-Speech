import requests
import time
API_KEY = ''  # Replace with your actual API key
HEADERS = {'authorization': API_KEY}
UPLOAD_ENDPOINT = 'https://api.assemblyai.com/v2/upload'
TRANSCRIPT_ENDPOINT = 'https://api.assemblyai.com/v2/transcript'
def upload(file_name):
    with open(file_name, 'rb') as f:
        response = requests.post(UPLOAD_ENDPOINT, headers=HEADERS, data=f)
    return response.json()['upload_url']
def transcribe(audio_url):
    response = requests.post(TRANSCRIPT_ENDPOINT, headers=HEADERS, json={'audio_url': audio_url})
    return response.json()['id']
def get_transcription_results(job_id):
    polling_endpoint = f"{TRANSCRIPT_ENDPOINT}/{job_id}"
    
    while True:
        response = requests.get(polling_endpoint, headers=HEADERS)
        data = response.json()
        
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return None, data['error']
        
        print("Waiting 30 seconds before polling again...")
        time.sleep(30)
