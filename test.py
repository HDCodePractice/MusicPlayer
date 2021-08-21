import asyncio
from asyncio.tasks import sleep
import os
from pytgcalls import GroupCallFactory
import pyrogram
import av
from config import Config
from av.error import ValueError
from util.AudioFileFifo import AudioFileFifo
from util.youtube import get_first_finalurl

API_HASH = Config.API_HASH
API_ID = Config.API_ID

CHAT_PEER = Config.CHAT  # chat or channel where you want to play audio
# SOURCE1 = "downloads/one.m4a"
SOURCE1 = "downloads/one.m4a"
SOURCE1 = get_first_finalurl("https://www.youtube.com/watch?v=_daTfgc4u3k")
SOURCE2 = "downloads/GoodTimes.m4a" # Audio file path or stream url: eg. https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_700KB.mp3
SOURCE3 = "downloads/music.m4a"
CLIENT_TYPE = GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM
# for Telethon uncomment line below
# CLIENT_TYPE = pytgcalls.GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON




async def main(client):
    await client.start()
    while not client.is_connected:
        await asyncio.sleep(1)

    group_call_factory = GroupCallFactory(client, CLIENT_TYPE)
    
    audio = AudioFileFifo()
    group_call_raw = group_call_factory.get_raw_group_call(on_played_data=audio.on_played_data)
    await group_call_raw.start(CHAT_PEER)
    while not group_call_raw.is_connected:
        await asyncio.sleep(1)
    
    print("call avdecode 1.....")
    task = asyncio.create_task(audio.avdecode(SOURCE1))
    await sleep(1000)
    print("cancel task 1")
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("main(): cancel_me is cancelled now")

    
    print("call avdecode 2.....")
    await audio.avdecode(SOURCE2)

    await pyrogram.idle()

if __name__ == "__main__":
    pyro_client = pyrogram.Client(
        Config.SESSION,
        api_hash=os.environ.get('API_HASH', API_HASH),
        api_id=os.environ.get('API_ID', API_ID)
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(pyro_client))