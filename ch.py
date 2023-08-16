import asyncio
import time
import os
from datetime import datetime
from telethon import TelegramClient, events

# Replace these values with your own
API_ID = 14858124
API_HASH = 'c5805198008e991a47a32fc4f7c6ec23'
BOT_TOKEN = '6664611261:AAHnrFyjH98u77NqDrJkh-WKy-RrVrh-eOA'
TMP_DOWNLOAD_DIRECTORY = 'downloaded_files'  # Directory to save downloaded files

bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern=r'^تحويل الى (صوتي|بصمة)$'))
async def convert_to_audio(event):
    if not event.reply_to_msg_id:
        await event.respond("**- يجب عليك الرد على الميديا المراد تحويلها**")
        return
    
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.respond("**- يجب عليك الرد على الميديا المراد تحويلها**")
        return
    
    input_str = event.pattern_match.group(1)
    await event.respond("**- جار التحويل انتظر قليلا ...**")
    
    try:
        start = datetime.now()
        c_time = time.time()
        downloaded_file_name = await bot.download_media(reply_message, TMP_DOWNLOAD_DIRECTORY)
    except Exception as e:
        await event.respond(str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
        await event.respond(
            f"- تم تنزيل الملف : {downloaded_file_name}\nالوقت المستغرق: {ms} من الثواني"
        )
        new_required_file_name = ""
        command_to_run = []
        voice_note = False
        
        if input_str == "بصمة":
            new_required_file_name = f"{TMP_DOWNLOAD_DIRECTORY}/voice_{str(round(time.time()))}.opus"
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-map",
                "0:a",
                "-codec:a",
                "libopus",
                "-b:a",
                "100k",
                "-vbr",
                "on",
                new_required_file_name,
            ]
            voice_note = True
        elif input_str == "صوتي":
            new_required_file_name = f"{TMP_DOWNLOAD_DIRECTORY}/mp3_{str(round(time.time()))}.mp3"
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-vn",
                new_required_file_name,
            ]
            voice_note = False
        else:
            await event.respond("**- هذه الصيغة غير مدعومة**")
            os.remove(downloaded_file_name)
            return
        
        process = await asyncio.create_subprocess_exec(
            *command_to_run,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        os.remove(downloaded_file_name)
        
        if os.path.exists(new_required_file_name):
            await bot.send_file(
                event.chat_id,
                new_required_file_name,
                force_document=False,
                voice_note=voice_note,
                reply_to=reply_message.id,
            )
            os.remove(new_required_file_name)

bot.start()
bot.run_until_disconnected()
