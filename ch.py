from telethon import TelegramClient, events, utils
from telethon.tl.types import InputFile

# Replace these with your own values
api_id = 12345678
api_hash = 'wretyu546uytr567uytr7u'
bot_token = '6104906824:AAFfdgn6fUd8DcDMOMkTNZavHYRKAGSSx8g'

client = TelegramClient('bot_session', api_id, api_hash)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("أرسل لي الفيديو لتحويله إلى رسالة صوتية.")

@client.on(events.NewMessage)
async def handle_message(event):
    if event.media and isinstance(event.media, InputFile):
        video_path = await event.download_media()
        voice_msg = utils.get_input_document(video_path, voice=True)
        await event.reply(file=voice_msg)
    else:
        await event.respond("الرجاء إرسال فيديو لتحويله إلى رسالة صوتية.")

async def main():
    await client.start(bot_token=bot_token)
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
