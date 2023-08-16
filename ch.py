import telebot

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('6104906824:AAFfdgn6fUd8DcDMOMkTNZavHYRKAGSSx8g')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to the audio conversion bot! Send me an audio or voice message.")

@bot.message_handler(content_types=['audio', 'voice'])
def handle_audio_or_voice(message):
    chat_id = message.chat.id

    if message.content_type == 'audio':
        file_info = bot.get_file(message.audio.file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)

        audio_filename = 'audio.ogg'
        with open(audio_filename, 'wb') as audio_file:
            audio_file.write(downloaded_file)

        voice_filename = 'voice.ogg'
        with open(voice_filename, 'wb') as voice_file:
            voice_file.write(downloaded_file)

        with open(voice_filename, 'rb') as voice_file:
            bot.send_voice(chat_id, voice_file)

        bot.send_message(chat_id, "Audio converted and sent as a voice message.")
    elif message.content_type == 'voice':
        file_info = bot.get_file(message.voice.file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)

        voice_filename = 'voice.ogg'
        with open(voice_filename, 'wb') as voice_file:
            voice_file.write(downloaded_file)

        with open(voice_filename, 'rb') as voice_file:
            bot.send_voice(chat_id, voice_file)

        bot.send_message(chat_id, "Voice message sent.")

bot.polling()
