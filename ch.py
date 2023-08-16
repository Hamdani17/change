import requests
import json

BOT_TOKEN = '6104906824:AAFfdgn6fUd8DcDMOMkTNZavHYRKAGSSx8g'
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

def send_message(chat_id, text):
    url = f'{BASE_URL}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': text,
    }
    response = requests.post(url, json=params)
    return response.json()

def get_file_info(file_id):
    url = f'{BASE_URL}/getFile'
    params = {
        'file_id': file_id,
    }
    response = requests.get(url, params=params)
    return response.json()

def download_file(file_path):
    url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}'
    response = requests.get(url)
    return response.content

def main():
    offset = None
    while True:
        updates_url = f'{BASE_URL}/getUpdates'
        params = {
            'offset': offset,
            'timeout': 30,
        }
        response = requests.get(updates_url, params=params)
        updates = response.json()['result']

        for update in updates:
            offset = update['update_id'] + 1
            message = update.get('message')

            if message and message.get('text') == '/start':
                send_message(message['chat']['id'], "Please send me a video.")
            elif message and message.get('video'):
                video_file_id = message['video']['file_id']
                file_info = get_file_info(video_file_id)
                file_path = file_info['result']['file_path']
                video_data = download_file(file_path)
                # Process the video data to extract audio
                # This part requires additional libraries for video processing

                # Send the audio back to the user
                # You'll need to implement this part as well

if __name__ == "__main__":
    main()
