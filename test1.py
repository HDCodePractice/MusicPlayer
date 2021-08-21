import asyncio
from asyncio.tasks import sleep
import os
from pytgcalls import GroupCallFactory
import pyrogram
import av
from config import Config

API_HASH = Config.API_HASH
API_ID = Config.API_ID

CHAT_PEER = Config.CHAT  # chat or channel where you want to play audio
SOURCE1 = "downloads/one.m4a"
SOURCE2 = "downloads/GoodTimes.m4a" # Audio file path or stream url: eg. https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_700KB.mp3
SOURCE3 = "downloads/music.m4a"
CLIENT_TYPE = GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM
# for Telethon uncomment line below
# CLIENT_TYPE = pytgcalls.GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON

# fifo = av.AudioFifo(format="s16le")
fifo = av.AudioFifo()
resampler = av.AudioResampler(format="s16", layout="stereo", rate=48000)


def on_played_data(gc, length):
    data = None
    if fifo :
        data = fifo.read(length / 4)
        if data:
            data = data.to_ndarray().tobytes()
    return data


async def main(client):
    global fifo,resampler
    await client.start()
    while not client.is_connected:
        await asyncio.sleep(1)

    group_call_factory = GroupCallFactory(client, CLIENT_TYPE)
    group_call_raw = group_call_factory.get_raw_group_call(on_played_data=on_played_data)
    await group_call_raw.start(CHAT_PEER)
    while not group_call_raw.is_connected:
        await asyncio.sleep(1)

    # group_call_raw.pause_playout()

    print(f"decode {SOURCE1}")
    _input = av.open(SOURCE1)
    for frame in _input.decode():
        if frame:
            frame.pts = None
            frame = resampler.resample(frame)
            fifo.write(frame)

    await sleep(3)

    print(f"decode {SOURCE2}")
    fifo = av.AudioFifo()
    resampler = av.AudioResampler(format="s16", layout="stereo", rate=48000)


    _input = av.open(SOURCE2)
    for frame in _input.decode():
        if frame:
            frame.pts = None
            frame = resampler.resample(frame)
            fifo.write(frame)
    
    await pyrogram.idle()

if __name__ == "__main__":
    pyro_client = pyrogram.Client(
        Config.SESSION,
        api_hash=os.environ.get('API_HASH', API_HASH),
        api_id=os.environ.get('API_ID', API_ID)
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(pyro_client))