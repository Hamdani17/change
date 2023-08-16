import telebot
from moviepy.editor import VideoFileClip
import os

# قم بإدخال توكن البوت الخاص بك هنا
bot_token = '6104906824:AAFfdgn6fUd8DcDMOMkTNZavHYRKAGSSx8g'
bot = telebot.TeleBot(bot_token)

@bot.message_handler(content_types=['video'])
def video_to_voice(message):
    try:
        video_message = message.video
        video_info = bot.get_file(video_message.file_id)
        video_path = video_info.file_path

        video_path_local = 'video.mp4'
        bot.download_file(video_path, video_path_local)

        video_clip = VideoFileClip(video_path_local)
        audio_clip = video_clip.audio
        audio_path = 'audio.ogg'
        audio_clip.write_audiofile(audio_path, codec='opus')

        audio = open(audio_path, 'rb')
        bot.send_voice(message.chat.id, audio)

        audio.close()

        os.remove(video_path_local)
        os.remove(audio_path)

    except Exception as e:
        bot.reply_to(message, "حدث خطأ أثناء معالجة الفيديو.")

bot.polling()
