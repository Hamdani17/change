import telebot
import os
from moviepy.editor import VideoFileClip

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('6104906824:AAFfdgn6fUd8DcDMOMkTNZavHYRKAGSSx8g')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to the audio extraction bot! Send me a video, audio, or voice message.")

@bot.message_handler(content_types=['video', 'audio', 'voice'])
def handle_media(message):
    chat_id = message.chat.id

    if message.content_type == 'video':
        file_info = bot.get_file(message.video.file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)

        video_filename = 'video.mp4'
        with open(video_filename, 'wb') as video_file:
            video_file.write(downloaded_file)

        audio_filename = 'audio.wav'
        video_clip = VideoFileClip(video_filename)
        video_clip.audio.write_audiofile(audio_filename)

        voice_filename = 'voice.ogg'
        with open(voice_filename, 'wb') as voice_file:
            voice_file.write(open(audio_filename, 'rb').read())

        with open(voice_filename, 'rb') as voice_file:
            bot.send_voice(chat_id, voice_file)

        bot.send_message(chat_id, "Audio extracted from the video and sent as a voice message.")

        # Clean up temporary files
        os.remove(video_filename)
        os.remove(audio_filename)
        os.remove(voice_filename)

    elif message.content_type in ['audio', 'voice']:
        file_info = bot.get_file(message.voice.file_id if message.content_type == 'voice' else message.audio.file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)

        voice_filename = 'voice.ogg'
        with open(voice_filename, 'wb') as voice_file:
            voice_file.write(downloaded_file)

        with open(voice_filename, 'rb') as voice_file:
            bot.send_voice(chat_id, voice_file)

        bot.send_message(chat_id, "Voice message sent.")

        os.remove(voice_filename)

bot.polling()
