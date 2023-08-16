import os
import requests
import json
from io import BytesIO
from subprocess import run, PIPE

# Replace 'YOUR_TOKEN' with your actual bot token
TOKEN = '6104906824:AAFfdgn6fUd8DcDMOMkTNZavHYRKAGSSx8g'

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, data=data)
    return response.json()

def process_video(file_id, chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/getFile"
    params = {'file_id': file_id}
    response = requests.get(url, params=params)
    file_path = response.json()["result"]["file_path"]
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

    video_data = requests.get(file_url).content
    with open('input_video.mp4', 'wb') as f:
        f.write(video_data)

    run(['ffmpeg', '-i', 'input_video.mp4', '-vn', '-acodec', 'pcm_s16le', 'audio.wav'], stdout=PIPE)

    with open('audio.wav', 'rb') as audio:
        url = f"https://api.telegram.org/bot{TOKEN}/sendAudio"
        files = {'audio': ('audio.wav', audio)}
        data = {
            'chat_id': chat_id
        }
        response = requests.post(url, data=data, files=files)

def handle_message(message):
    chat_id = message['chat']['id']
    text = message.get('text', '')

    if text == '/start':
        send_message(chat_id, "Send a video to extract audio from.")
    elif 'video' in message:
        video_file_id = message['video']['file_id']
        process_video(video_file_id, chat_id)

def main():
    offset = None
    while True:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        params = {'offset': offset}
        response = requests.get(url, params=params)
        data = response.json()

        if data['ok']:
            for update in data['result']:
                offset = update['update_id'] + 1
                if 'message' in update:
                    handle_message(update['message'])

if __name__ == '__main__':
    main()
