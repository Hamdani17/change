import telebot

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
    bot.send_message(chat_id, "Send me a voice message to record.")

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    chat_id = message.chat.id
    if chat_id in record_state and record_state[chat_id]:
        file_info = bot.get_file(message.voice.file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)
        
        voice_filename = 'voice.ogg'
        with open(voice_filename, 'wb') as voice_file:
            voice_file.write(downloaded_file)
        
        with open(voice_filename, 'rb') as voice_file:
            bot.send_voice(chat_id, voice_file)
        
        bot.send_message(chat_id, "Voice message recorded and sent.")
        record_state[chat_id] = False
    else:
        bot.send_message(chat_id, "Send /record to start recording first.")

bot.polling()
