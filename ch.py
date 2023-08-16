import requests
import json

TOKEN = '6104906824:AAFfdgn6fUd8DcDMOMkTNZavHYRKAGSSx8g'

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    return response.json()

def get_file_path(file_id):
    url = f"https://api.telegram.org/bot{TOKEN}/getFile"
    payload = {'file_id': file_id}
    response = requests.get(url, params=payload)
    data = response.json()
    file_path = data['result']['file_path']
    return file_path

def download_file(file_path):
    url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    response = requests.get(url)
    return response.content

def main():
    # Replace with your logic to receive and parse updates
    chat_id = 'RECIPIENT_CHAT_ID'  # Replace with the actual recipient's chat ID
    message = '/start'  # Replace with the received message

    if message == '/start':
        send_message(chat_id, "Please send a video.")

        # Replace with your logic to receive and parse updates
        video_file_id = 'RECEIVED_VIDEO_FILE_ID'  # Replace with the actual received video file ID

        file_path = get_file_path(video_file_id)
        video_data = download_file(file_path)

        # Here you can process the video_data to extract audio and send it back

if __name__ == "__main__":
    main()
