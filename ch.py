import telebot
import os
from pydub import AudioSegment

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('6104906824:AAFfdgn6fUd8DcDMOMkTNZavHYRKAGSSx8g')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! Send me a video, and I'll extract and send back the audio.")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    try:
        # Download the video
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        video_path = 'input_video.mp4'
        with open(video_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Extract audio from the video
        audio_path = 'extracted_audio.wav'
        video = AudioSegment.from_file(video_path)
        audio = video.export(audio_path, format='wav')

        # Send the extracted audio back
        bot.send_audio(message.chat.id, audio, title='Extracted Audio')

        # Clean up the temporary files
        os.remove(video_path)
        os.remove(audio_path)
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, "Send me a video to extract audio!")

# Start the bot
bot.polling()
