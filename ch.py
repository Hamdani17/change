import telebot
import subprocess
import os
# Replace with your actual Telegram bot token
bot_token = '6664611261:AAHnrFyjH98u77NqDrJkh-WKy-RrVrh-eOA'
bot = telebot.TeleBot(bot_token)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    video_file_id = message.video.file_id
    video_info = bot.get_file(video_file_id)
    video_path = video_info.file_path
    video_url = f'https://api.telegram.org/file/bot{bot_token}/{video_path}'

    audio_file_path = 'output_audio.ogg'
    
    # Using FFmpeg to extract audio from the video
    subprocess.call(['ffmpeg', '-i', video_url, '-vn', audio_file_path])

    # Send the extracted audio as a voice message
    voice = open(audio_file_path, 'rb')
    bot.send_voice(message.chat.id, voice)
    voice.close()

    # Save the audio in the same location as the script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    saved_audio_path = os.path.join(script_directory, audio_file_path)
    os.rename(audio_file_path, saved_audio_path)

if __name__ == '__main__':
    bot.polling()
