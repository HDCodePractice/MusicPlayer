#MIT License

#Copyright (c) 2021 SUBIN 老房东

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
import os
import asyncio
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from config import Config
import ffmpeg
from pyrogram import emoji
from pyrogram.utils import MAX_CHANNEL_ID
from pyrogram.methods.messages.download_media import DEFAULT_DOWNLOAD_DIR
from pytgcalls import GroupCallFactory
from util.AudioFileFifo import AudioFileFifo
import signal
import wget
from asyncio import sleep
from pyrogram import Client
from youtube_dl import YoutubeDL
from util.youtube import get_first_finalurl, youtube_downaudio
from os import path
bot = Client(
    "Musicplayervc",
    Config.API_ID,
    Config.API_HASH,
    workdir=Config.WORKDIR,
    bot_token=Config.BOT_TOKEN
)
bot.start()
e=bot.get_me()
USERNAME=e.username

from user import USER

STREAM_URL=Config.STREAM_URL
CHAT=Config.CHAT
GROUP_CALLS = {}
FFMPEG_PROCESSES = {}
RADIO={6}
LOG_GROUP=Config.LOG_GROUP
DURATION_LIMIT=Config.DURATION_LIMIT
DELAY=Config.DELAY
playlist=Config.playlist
msg=Config.msg


ydl_opts = {
    "format": "bestaudio[ext=m4a]",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)
async def youtube(url: str) -> str:
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, ydl.download, [url])
        # ydl.download([url])
    except Exception as e:
        print(e)
        pass
    return path.join("downloads", f"{info['id']}.{info['ext']}")

class MusicPlayer(object):
    CLIENT_TYPE = GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM
    fifo_task = None

    def __init__(self):
        # self.group_call = GroupCallFactory(USER,self.CLIENT_TYPE).get_file_group_call()
        self.audio_fifo = AudioFileFifo()
        self.group_call = GroupCallFactory(USER,self.CLIENT_TYPE).get_raw_group_call()
        self.chat_id = None


    async def send_playlist(self):
        if not playlist:
            pl = f"{emoji.NO_ENTRY} Playlist is empty!!\n{emoji.NO_ENTRY} 播放列表里嘛都木有"
        else:
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4].split('(tg://user?id=')[0]}\n"
                for i, x in enumerate(playlist)
            ])
        if msg.get('playlist') is not None:
            await msg['playlist'].delete()
        msg['playlist'] = await self.send_text(pl)

    async def skip_current_playing(self):
        group_call = self.group_call
        if not playlist:
            return
        if len(playlist) == 1:
            await mp.start_radio()
            return
        client = group_call.client
        download_dir = os.path.join(client.workdir, DEFAULT_DOWNLOAD_DIR)
        group_call.input_filename = os.path.join(
            download_dir,
            f"{playlist[1][5]}.raw"
        )
        # remove old track from playlist
        old_track = playlist.pop(0)
        print(f"- START PLAYING: {playlist[0][1]}")
        await self.send_photo(playlist[0])
        if LOG_GROUP:
            await self.send_playlist()
        os.remove(os.path.join(
            download_dir,
            f"{old_track[5]}.raw")
        )
        if len(playlist) == 1:
            return
        await self.download_audio(playlist[1])

    async def send_text(self, text):
        group_call = self.group_call
        client = group_call.client
        chat_id = LOG_GROUP
        message = await bot.send_message(
            chat_id,
            text,
            disable_web_page_preview=True,
            disable_notification=True
        )
        return message

    async def send_photo(self,track):
        if LOG_GROUP:
            chat_id = LOG_GROUP
            buttons = [[
                InlineKeyboardButton('再次点播', callback_data=f'research={track[2]}'),
                InlineKeyboardButton('加入我的收藏', callback_data=f'addme={track[2]}'),
            ],[
                InlineKeyboardButton('来源',url=track[2])
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            phtoturl = track[6].split('?')[0]
            message = await bot.send_photo(
                chat_id,
                photo=phtoturl,
                caption=f"`{track[1]}`\n点播者: {track[4]} ",
                reply_markup=reply_markup,
                disable_notification=True
            )
            return message
        return None

    async def download_audio(self, song):
        group_call = self.group_call
        client = group_call.client
        raw_file = os.path.join(client.workdir, DEFAULT_DOWNLOAD_DIR,
                                f"{song[5]}.raw")
        #if os.path.exists(raw_file):
            #os.remove(raw_file)
        if not os.path.isfile(raw_file):
            # credits: https://t.me/c/1480232458/6825
            #os.mkfifo(raw_file)
            if song[3] == "telegram":
                original_file = await bot.download_media(f"{song[2]}")
            elif song[3] == "youtube":
                original_file = await youtube(song[2])
            else:
                original_file=wget.download(song[2])
            ffmpeg.input(original_file).output(
                raw_file,
                format='s16le',
                acodec='pcm_s16le',
                ac=2,
                ar='48k',
                loglevel='error'
            ).overwrite_output().run()
            os.remove(original_file)


    async def start_radio(self):
        group_call = self.group_call
        await group_call.stop()
        if not group_call.is_connected:
            await group_call.start(CHAT)
        
        while not group_call.is_connected:
            print("wait connect")
            await asyncio.sleep(1)
        print(STREAM_URL)
        afile = await youtube_downaudio(STREAM_URL)
        print(f"download {afile} fin")
        audio_fifo = self.audio_fifo
        if os.path.isfile(afile):
            self.audio_task = asyncio.create_task(audio_fifo.avdecode(afile))
            audio_fifo.loop = asyncio.get_event_loop()
            self.group_call.on_played_data = audio_fifo.on_played_data
            audio_fifo.on_playout_ended(self.start_radio)
            try:
                RADIO.remove(0)
            except:
                pass
            try:
                RADIO.add(1)
            except:
                pass
        else:
            print("No File Found\nSleeping...\n\n文件没找到\n晚安...")


    async def stop_radio(self):
        group_call = self.group_call
        if group_call:
            playlist.clear()   
            self.audio_task.cancel()
            try:
                RADIO.remove(1)
            except:
                pass
            try:
                RADIO.add(0)
            except:
                pass

    async def start_call(self):
        group_call = self.group_call
        await group_call.start(CHAT)
    
    async def delete(self, message):
        if message.chat.type == "supergroup":
            await sleep(DELAY)
            try:
                await message.delete()
            except:
                pass
        



mp = MusicPlayer()


# pytgcalls handlers

@mp.group_call.on_network_status_changed
async def network_status_changed_handler(context, is_connected: bool):
    if is_connected:
        mp.chat_id = MAX_CHANNEL_ID - context.full_chat.id
    else:
        mp.chat_id = None

# raw group call 没有 ended的回调
# @mp.group_call.on_playout_ended
# async def playout_ended_handler(_, __):
#     if not playlist:
#         await mp.start_radio()
#     else:
#         await mp.skip_current_playing()
