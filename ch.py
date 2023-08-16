import telebot
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO

# استبدال "TOKEN" بتوكن البوت الخاص بك
bot = telebot.TeleBot("6104906824:AAFfdgn6fUd8DcDMOMkTNZavHYRKAGSSx8g")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "مرحبًا! يرجى إرسال فيديو لتحويله إلى رسالة صوتية.")

@bot.message_handler(content_types=['video'])
def convert_to_audio(message):
    chat_id = message.chat.id
    file_id = message.video.file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    
    video_path = f"https://api.telegram.org/file/botTOKEN/{file_path}"
    
    # تحويل الفيديو إلى ملف صوتي
    video = AudioSegment.from_file(video_path, format="webm")
    audio = video.set_channels(1).set_frame_rate(16000)
    
    # تحويل الصوت إلى بيانات قابلة للإرسال
    audio_io = BytesIO()
    audio.export(audio_io, format="ogg")
    audio_io.seek(0)
    
    # إرسال الرسالة الصوتية إلى المستخدم
    bot.send_voice(chat_id, audio_io, reply_to_message_id=message.message_id)

# بدء استماع البوت
bot.polling()
