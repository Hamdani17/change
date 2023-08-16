import telebot
import os
from pydub import AudioSegment
from pydub.playback import play

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('6104906824:AAFfdgn6fUd8DcDMOMkTNZavHYRKAGSSx8g')

@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    try:
        # Download the audio file
        audio_info = bot.get_file(message.audio.file_id)
        audio_file = bot.download_file(audio_info.file_path)

        # Save the downloaded audio to a file
        audio_path = 'original_audio.ogg'
        with open(audio_path, 'wb') as f:
            f.write(audio_file)

        # Load the original audio
        original_audio = AudioSegment.from_file(audio_path, format='ogg')

        # Simulate "recording" by playing the audio
        play(original_audio)

        # Save the "recorded" audio to a file
        recorded_audio_path = 'recorded_audio.ogg'
        with open(recorded_audio_path, 'wb') as f:
            original_audio.export(f, format='ogg')

        # Send the "recorded" audio back to the user
        with open(recorded_audio_path, 'rb') as f:
            bot.send_audio(message.chat.id, f)

        # Clean up temporary files
        os.remove(audio_path)
        os.remove(recorded_audio_path)

    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "An error occurred.")

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    bot.send_message(message.chat.id, "Please send an audio file.")

# Start the bot
bot.polling()
