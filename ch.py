import telebot
import subprocess

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

    # Clean up the temporary audio file
    subprocess.call(['rm', audio_file_path])

if __name__ == '__main__':
    bot.polling()
