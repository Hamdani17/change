import telebot
from telebot import types
import os

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('6104906824:AAFfdgn6fUd8DcDMOMkTNZavHYRKAGSSx8g')

# Dictionary to store user states (whether they are waiting for a video or not)
user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_states[user_id] = 'waiting_for_video'
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    item = types.KeyboardButton("Send Video")
    markup.add(item)
    
    bot.send_message(user_id, "Please send a video:", reply_markup=markup)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    user_id = message.from_user.id
    if user_id in user_states and user_states[user_id] == 'waiting_for_video':
        user_states[user_id] = 'not_waiting'
        
        file_info = bot.get_file(message.video.file_id)
        file_path = file_info.file_path
        
        video_path = os.path.join("videos", file_path)
        voice_path = os.path.join("voices", f"{user_id}_voice.ogg")
        
        downloaded_file = bot.download_file(file_path)
        with open(video_path, 'wb') as f:
            f.write(downloaded_file)
        
        os.system(f"ffmpeg -i {video_path} -vn -acodec libopus {voice_path}")
        
        voice_file = open(voice_path, 'rb')
        bot.send_voice(user_id, voice_file)
        
        os.remove(video_path)
        os.remove(voice_path)
        
        bot.send_message(user_id, "Here is the voice from the video.")
    else:
        bot.send_message(user_id, "Please start with /start to initiate the process.")

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    user_id = message.from_user.id
    if user_id in user_states and user_states[user_id] == 'waiting_for_video':
        bot.send_message(user_id, "Please send a video using the provided button.")
    else:
        bot.send_message(user_id, "Please start with /start to initiate the process.")

bot.polling()
