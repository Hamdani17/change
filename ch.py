import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace 'YOUR_TOKEN' with your actual bot token
TOKEN = '6104906824:AAFfdgn6fUd8DcDMOMkTNZavHYRKAGSSx8g'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send a video to extract audio from.")

def process_video(update: Update, context: CallbackContext) -> None:
    # Get the file id of the received video
    file_id = update.message.video.file_id

    # Download the video file
    video_file = context.bot.get_file(file_id)
    video_file.download('input_video.mp4')

    # Use ffmpeg to extract audio
    os.system("ffmpeg -i input_video.mp4 -vn -acodec pcm_s16le audio.wav")

    # Send the extracted audio back to the user
    with open('audio.wav', 'rb') as audio:
        update.message.reply_audio(audio)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.video, process_video))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
