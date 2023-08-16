import telebot
import os
from moviepy.editor import VideoFileClip

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('6104906824:AAFfdgn6fUd8DcDMOMkTNZavHYRKAGSSx8g')

waiting_for_video = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to the video to audio bot! Send /convert to start the conversion.")

@bot.message_handler(commands=['convert'])
def convert(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Please send me a video to convert to audio.")
    waiting_for_video[chat_id] = True

@bot.message_handler(content_types=['video'])
def convert_to_audio(message):
    chat_id = message.chat.id
    if chat_id in waiting_for_video and waiting_for_video[chat_id]:
        file_info = bot.get_file(message.video.file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)

        video_filename = 'video.mp4'
        audio_filename = 'audio.ogg'

        with open(video_filename, 'wb') as video_file:
            video_file.write(downloaded_file)

        video_clip = VideoFileClip(video_filename)
        video_clip.audio.write_audiofile(audio_filename)

        with open(audio_filename, 'rb') as audio_file:
            bot.send_audio(chat_id, audio_file)

        # Clean up temporary files
        os.remove(video_filename)
        os.remove(audio_filename)

        bot.send_message(chat_id, "Here is the audio extracted from the video.")
        waiting_for_video[chat_id] = False
    else:
        bot.send_message(chat_id, "Send /convert to start the conversion first.")

bot.polling()
