import telebot
import os
from pydub import AudioSegment
from io import BytesIO

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('6104906824:AAFfdgn6fUd8DcDMOMkTNZavHYRKAGSSx8g')

@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    try:
        # Download the audio file
        file_info = bot.get_file(message.audio.file_id)
        file_path = file_info.file_path
        file_data = bot.download_file(file_path)
        
        # Convert audio data to an AudioSegment
        audio = AudioSegment.from_file(BytesIO(file_data), format="ogg")
        
        # Export the audio as WAV
        wav_path = "temp.wav"
        audio.export(wav_path, format="wav")
        
        # Send the processed voice message
        voice_message = open(wav_path, 'rb')
        bot.send_voice(message.chat.id, voice_message)
        
        # Clean up temporary files
        os.remove(wav_path)
        
    except Exception as e:
        bot.reply_to(message, "An error occurred while processing the audio.")

@bot.message_handler(func=lambda message: True)
def handle_other(message):
    bot.reply_to(message, "Please send an audio message.")

bot.polling()
