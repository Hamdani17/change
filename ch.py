import telebot
import os

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('6104906824:AAFfdgn6fUd8DcDMOMkTNZavHYRKAGSSx8g')

record_state = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to the audio recording bot! Send /record to start recording.")

@bot.message_handler(commands=['record'])
def record(message):
    chat_id = message.chat.id
    record_state[chat_id] = True
    bot.send_message(chat_id, "Send me a voice message or audio file to record.")

@bot.message_handler(content_types=['voice', 'audio'])
def handle_audio(message):
    chat_id = message.chat.id
    if chat_id in record_state and record_state[chat_id]:
        file_info = bot.get_file(message.voice.file_id if message.content_type == 'voice' else message.audio.file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)
        
        if message.content_type == 'voice':
            audio_filename = 'voice.ogg'
        else:
            audio_filename = 'audio.ogg'
        
        with open(audio_filename, 'wb') as audio_file:
            audio_file.write(downloaded_file)
        
        with open(audio_filename, 'rb') as audio_file:
            bot.send_audio(chat_id, audio_file)
        
        bot.send_message(chat_id, "Audio recorded and sent.")
        record_state[chat_id] = False
        os.remove(audio_filename)
    else:
        bot.send_message(chat_id, "Send /record to start recording first.")

bot.polling()
