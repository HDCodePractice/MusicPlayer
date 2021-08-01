#MIT License

#Copyright (c) 2021 SUBIN 老房东 Sichengthebest

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
from youtube_dl import YoutubeDL
from config import Config
from pyrogram import Client, filters, emoji
from pyrogram.methods.messages.download_media import DEFAULT_DOWNLOAD_DIR
from pyrogram.types import Message
from utils import mp, RADIO, USERNAME, FFMPEG_PROCESSES
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from youtube_search import YoutubeSearch
from pyrogram import Client
from aiohttp import ClientSession
import signal
import re
U=USERNAME
ADMIN_ONLY=Config.ADMIN_ONLY
DURATION_LIMIT = Config.DURATION_LIMIT
session = ClientSession()
playlist=Config.playlist
msg = Config.msg
ADMINS=Config.ADMINS
CHAT=Config.CHAT
LOG_GROUP=Config.LOG_GROUP
playlist=Config.playlist

@Client.on_message(filters.command(["play", f"play@{U}","y"]) & (filters.chat([CHAT,LOG_GROUP]) | filters.private) | filters.audio & filters.private)
async def yplay(_, message: Message):
    if ADMIN_ONLY == "Y":
        admins=Config.ADMINS
        grpadmins=await _.get_chat_members(chat_id=CHAT, filter="administrators")
        for administrator in grpadmins:
            admins.append(administrator.user.id)
        if message.from_user.id not in admins:
            m=await message.reply_sticker("CAADBQADsQIAAtILIVYld1n74e3JuQI")
            await mp.delete(m)
            await message.delete()
            return
    type=""
    yturl=""
    ysearch=""
    if message.audio:
        type="audio"
        m_audio = message
    elif message.reply_to_message and message.reply_to_message.audio:
        type="audio"
        m_audio = message.reply_to_message
    else:
        if message.reply_to_message:
            link=message.reply_to_message.text
            regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
            match = re.match(regex,link)
            if match:
                type="youtube"
                yturl=link
        elif " " in message.text:
            text = message.text.split(" ", 1)
            query = text[1]
            regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
            match = re.match(regex,query)
            if match:
                type="youtube"
                yturl=query
            else:
                type="query"
                ysearch=query
        else:
            d=await message.reply_text("Please use /play <song name> or /y <song name> to search and play, you can also search on youtube by replying to this bot.\n请使用/play <歌曲名> 或者使用 /y <歌曲名> 来搜索播放，你也可以reply本机器人在youtube上进行搜索")
            await mp.delete(d)
            await message.delete()
            return
    user=f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    group_call = mp.group_call
    if type=="audio":
        if round(m_audio.audio.duration / 60) > DURATION_LIMIT:
            d=await message.reply_text(f"❌ Audios longer than {DURATION_LIMIT} minute(s) aren't allowed, the provided audio is {round(m_audio.audio.duration/60)} minute(s)\n❌ 此机器人放不了比{DURATION_LIMIT}分钟跟长的歌，此歌有{round(m_audio.audio.duration/60)}分钟长")
            await mp.delete(d)
            await message.delete()
            return
        if playlist and playlist[-1][2] \
                == m_audio.audio.file_id:
            d=await message.reply_text(f"{emoji.ROBOT} Already added in playlist\nPlaylist里已经有了！")
            await mp.delete(d)
            await message.delete()
            return
        # 加入fileid
        data={1:m_audio.audio.title, 2:m_audio.audio.file_id, 3:"telegram", 4:user, 5:m_audio.audio.file_id, 6:None}
        playlist.append(data)
        if len(playlist) == 1:
            m_status = await message.reply_text(
                f"{emoji.INBOX_TRAY} Downloading and Processing...\n{emoji.INBOX_TRAY} 小水管在尽力下载..."
            )
            await mp.download_audio(playlist[0])
            if 1 in RADIO:
                if group_call:
                    group_call.input_filename = ''
                    RADIO.remove(1)
                    RADIO.add(0)
                process = FFMPEG_PROCESSES.get(CHAT)
                if process:
                    process.send_signal(signal.SIGTERM)
            if not group_call.is_connected:
                await mp.start_call()
            file=playlist[0][5]
            group_call.input_filename = os.path.join(
                _.workdir,
                DEFAULT_DOWNLOAD_DIR,
                f"{file}.raw"
            )

            await m_status.delete()
            print(f"- START PLAYING: {playlist[0][1]}")
            await mp.send_photo(playlist[0])
        if not playlist:
            pl = f"{emoji.NO_ENTRY} Empty playlist\nPlaylist是空的"
        else:   
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        for track in playlist[:2]:
            await mp.download_audio(track)
        if message.chat.type == "private":
            await message.reply_text(pl)        
        elif LOG_GROUP:
            await mp.send_playlist()
        else:
            k=await message.reply_text(pl)
            await mp.delete(k)
    if type=="youtube" or type=="query":
        if type=="youtube":
            msg = await message.reply_text("⚡️ **Fetching Song From YouTube...**\n⚡️ **正在从YouTube加载歌曲...**")
            url=yturl
        elif type=="query":
            try:
                msg = await message.reply_text("⚡️ **Fetching Song From YouTube...**\n⚡️ **正在从YouTube加载歌曲...**")
                ytquery=ysearch
                results = YoutubeSearch(ytquery, max_results=1).to_dict()
                url = f"https://youtube.com{results[0]['url_suffix']}"
                title = results[0]["title"][:40]
            except Exception as e:
                await msg.edit(
                    "Song not found.\nTry inline mode...\n==================\n啥么都没找到"
                )
                print(str(e))
                return
        else:
            return
        ydl_opts = {
            "geo-bypass": True,
            "nocheckcertificate": True
        }
        ydl = YoutubeDL(ydl_opts)
        info = ydl.extract_info(url, False)
        duration = round(info["duration"] / 60)
        title= info["title"]
        if int(duration) > DURATION_LIMIT:
            k=await message.reply_text(f"❌ Videos longer than {DURATION_LIMIT} minute(s) aren't allowed, the provided video is {duration} minute(s)\n此机器人放不了比{DURATION_LIMIT}分钟跟长的歌，此歌有{duration}分钟长")
            await mp.delete(k)
            await message.delete()
            return
        # data里加入5 文件id/6图片url
        data={1:title, 2:url, 3:"youtube", 4:user,5:info['id'],6:info['thumbnails'][0]['url']}
        playlist.append(data)
        group_call = mp.group_call
        client = group_call.client
        if len(playlist) == 1:
            m_status = await msg.edit(
                f"{emoji.INBOX_TRAY} Downloading and Processing...{emoji.INBOX_TRAY} 小水管在尽力下载..."
            )
            await mp.download_audio(playlist[0])
            if 1 in RADIO:
                if group_call:
                    group_call.input_filename = ''
                    RADIO.remove(1)
                    RADIO.add(0)
                process = FFMPEG_PROCESSES.get(CHAT)
                if process:
                    process.send_signal(signal.SIGTERM)
            if not group_call.is_connected:
                await mp.start_call()
            file=playlist[0][5]
            group_call.input_filename = os.path.join(
                client.workdir,
                DEFAULT_DOWNLOAD_DIR,
                f"{file}.raw"
            )

            await m_status.delete()
            print(f"- START PLAYING: {playlist[0][1]}")
            await mp.send_photo(playlist[0])
        else:
            await msg.delete()
        if not playlist:
            pl = f"{emoji.NO_ENTRY} Empty playlist\nPlaylist是空的"
        else:
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        for track in playlist[:2]:
            await mp.download_audio(track)
        if message.chat.type == "private":
            await message.reply_text(pl)
        if LOG_GROUP:
            await mp.send_playlist()
        else:
            k=await message.reply_text(pl)
            await mp.delete(k)
    await message.delete()

@Client.on_message(filters.command(["player", f"player@{U}"]) & (filters.chat([CHAT,LOG_GROUP]) | filters.private))
async def player(_, m: Message):
    if not playlist:
        k=await m.reply_text(f"{emoji.NO_ENTRY} No songs are playing\n{emoji.NO_ENTRY} 现在不在播放音乐")
        await mp.delete(k)
        await m.delete()
        return
    else:
        pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
            f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
            for i, x in enumerate(playlist)
            ])
    if m.chat.type == "private":
        await m.reply_text(
            pl,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔄", callback_data="replay"),
                        InlineKeyboardButton("⏯", callback_data="pause"),
                        InlineKeyboardButton("⏩", callback_data="skip")
                    
                    ],

                ]
                )
        )
    else:
        if msg.get('playlist') is not None:
            await msg['playlist'].delete()
        msg['playlist'] = await m.reply_text(
            pl,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔄", callback_data="replay"),
                        InlineKeyboardButton("⏯", callback_data="pause"),
                        InlineKeyboardButton("⏩", callback_data="skip")
                    
                    ],

                ]
                )
        )
    await m.delete()

@Client.on_message(filters.command(["skip", f"skip@{U}"]) & filters.user(ADMINS) & (filters.chat([CHAT,LOG_GROUP]) | filters.private))
async def skip_track(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        k=await m.reply("Nothing Playing\n现在不在播放音乐")
        await mp.delete(k)
        await m.delete()
        return
    if len(m.command) == 1:
        await mp.skip_current_playing()
        if not playlist:
            pl = f"{emoji.NO_ENTRY} Empty playlist\nPlaylist是空的"
        else:
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
            f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
            for i, x in enumerate(playlist)
            ])
        if m.chat.type == "private":
            await m.reply_text(pl)
        if LOG_GROUP:
            await mp.send_playlist()
        else:
            k=await m.reply_text(pl)
            await mp.delete(k)
    else:
        try:
            items = list(dict.fromkeys(m.command[1:]))
            items = [int(x) for x in items if x.isdigit()]
            items.sort(reverse=True)
            text = []
            for i in items:
                if 2 <= i <= (len(playlist) - 1):
                    audio = f"{playlist[i].audio.title}"
                    playlist.pop(i)
                    text.append(f"{emoji.WASTEBASKET} {i}. **{audio}**")
                else:
                    text.append(f"{emoji.CROSS_MARK} {i}")
            k=await m.reply_text("\n".join(text))
            await mp.delete(k)
            if not playlist:
                pl = f"{emoji.NO_ENTRY} Empty Playlist\nPlaylist是空的"
            else:
                pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
                    for i, x in enumerate(playlist)
                    ])
            if m.chat.type == "private":
                await m.reply_text(pl)
            if LOG_GROUP:
                await mp.send_playlist()
            else:
                k=await m.reply_text(pl)
                await mp.delete(k)
        except (ValueError, TypeError):
            k=await m.reply_text(f"{emoji.NO_ENTRY} Invalid input",
                                       disable_web_page_preview=True)
            await mp.delete(k)
    await m.delete()


@Client.on_message(filters.command(["join", f"join@{U}"]) & filters.user(ADMINS) & (filters.chat([CHAT,LOG_GROUP]) | filters.private))
async def join_group_call(client, m: Message):
    group_call = mp.group_call
    if group_call.is_connected:
        k=await m.reply_text(f"{emoji.ROBOT} Already joined voice chat\n已经在voice chat里头了！")
        await mp.delete(k)
        await m.delete()
        return
    await mp.start_call()
    chat = await client.get_chat(CHAT)
    k=await m.reply_text(f"Succesfully Joined voice chat in {chat.title}\n成功的加入了{chat.title}的voice chat")
    await mp.delete(k)
    await m.delete()


@Client.on_message(filters.command(["leave", f"leave@{U}"]) & filters.user(ADMINS))
async def leave_voice_chat(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        k=await m.reply_text("Not joined any voice chat yet.\n我都没有加入voice chat，我还咋么离开呀？")
        await mp.delete(k)
        await m.delete()
        return
    playlist.clear()
    if 1 in RADIO:
        await mp.stop_radio()
    group_call.input_filename = ''
    await group_call.stop()
    k=await m.reply_text("Left the voice chat\n已退出voice chat")
    await mp.delete(k)
    await m.delete()


@Client.on_message(filters.command(["vc", f"vc@{U}"]) & filters.user(ADMINS) & (filters.chat([CHAT,LOG_GROUP]) | filters.private))
async def list_voice_chat(client, m: Message):
    group_call = mp.group_call
    if group_call.is_connected:
        chat_id = int("-100" + str(group_call.full_chat.id))
        chat = await client.get_chat(chat_id)
        k=await m.reply_text(
            f"{emoji.MUSICAL_NOTES} **Currently in the voice chat**:\n"
            f"- **{chat.title}**"
        )
    else:
        k=await m.reply_text(emoji.NO_ENTRY
                                   + "Didn't join any voice chat yet\n暂时没加入voice chat")
    await mp.delete(k)
    await m.delete()


@Client.on_message(filters.command(["stop", f"stop@{U}"]) & filters.user(ADMINS) & (filters.chat([CHAT,LOG_GROUP]) | filters.private))
async def stop_playing(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        k=await m.reply_text("Nothing playing to stop.\n啥么都不在播放！")
        await mp.delete(k)
        await m.delete()
        return
    if 1 in RADIO:
        await mp.stop_radio()
    group_call.stop_playout()
    k=await m.reply_text(f"{emoji.STOP_BUTTON} Stopped playing.\n以停止播放。")
    playlist.clear()
    await mp.delete(k)
    await m.delete()


@Client.on_message(filters.command(["replay", f"replay@{U}"]) & filters.user(ADMINS) & (filters.chat([CHAT,LOG_GROUP]) | filters.private))
async def restart_playing(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        k=await m.reply_text("Nothing playing to replay.\n啥么都不在播放！")
        await mp.delete(k)
        await m.delete()
        return
    if not playlist:
        k=await m.reply_text("Empty Playlist.\nPlaylist是空的")
        await mp.delete(k)
        await m.delete()
        return
    group_call.restart_playout()
    k=await m.reply_text(
        f"{emoji.COUNTERCLOCKWISE_ARROWS_BUTTON}  "
        "Playing from the beginning...\n从新开始播放playlist..."
    )
    await mp.delete(k)
    await m.delete()


@Client.on_message(filters.command(["pause", f"pause@{U}"]) & filters.user(ADMINS) & (filters.chat([CHAT,LOG_GROUP]) | filters.private))
async def pause_playing(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        k=await m.reply_text("Nothing playing to pause.\n啥么都不在播放！")
        await mp.delete(k)
        await m.delete()
        return
    mp.group_call.pause_playout()
    k=await m.reply_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Paused.\n已暂停。",
                               quote=False)
    await mp.delete(k)
    await m.delete()



@Client.on_message(filters.command(["resume", f"resume@{U}"]) & filters.user(ADMINS) & (filters.chat([CHAT,LOG_GROUP]) | filters.private))
async def resume_playing(_, m: Message):
    if not mp.group_call.is_connected:
        k=await m.reply_text("Nothing paused to resume.啥么都没暂停！")
        await mp.delete(k)
        await m.delete()
        return
    mp.group_call.resume_playout()
    k=await m.reply_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Resumed.\n已从新开始播放。",
                               quote=False)
    await mp.delete(k)
    await m.delete()

@Client.on_message(filters.command(["clean", f"clean@{U}"]) & filters.user(ADMINS) & (filters.chat([CHAT,LOG_GROUP]) | filters.private))
async def clean_raw_pcm(client, m: Message):
    download_dir = os.path.join(client.workdir, DEFAULT_DOWNLOAD_DIR)
    all_fn: list[str] = os.listdir(download_dir)
    for track in playlist[:2]:
        track_fn = f"{track[1]}.raw"
        if track_fn in all_fn:
            all_fn.remove(track_fn)
    count = 0
    if all_fn:
        for fn in all_fn:
            if fn.endswith(".raw"):
                count += 1
                os.remove(os.path.join(download_dir, fn))
    k=await m.reply_text(f"{emoji.WASTEBASKET} Cleaned {count} files")
    await mp.delete(k)
    await m.delete()

@Client.on_message(filters.command(["vol", f"vol@{U}"]) & filters.user(ADMINS) & (filters.chat([CHAT,LOG_GROUP]) | filters.private))
async def volume(_, m: Message):
    usage = "**使用方法:**\n/vol [1-200]"
    group_call = mp.group_call
    if not group_call.is_connected:
        k=await m.reply_text("没有任何播放可以设置音量。")
        await mp.delete(k)
        await m.delete()
        return
    volume = int(m.text.split(None, 1)[1])
    if (volume < 1) or (volume > 200):
        k=await m.reply_text(usage, quote=False)
    else:
        try:
            await group_call.set_my_volume(volume=volume)
            k=await m.reply_text(f"**音量已经设置为 {volume}**", quote=False)
        except ValueError:
            k=await m.reply_text(usage, quote=False)
    await mp.delete(k)
    await m.delete()

@Client.on_message(filters.command(["mute", f"mute@{U}"]) & filters.user(ADMINS) & (filters.chat([CHAT,LOG_GROUP]) | filters.private))
async def mute(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        k=await m.reply_text("Nothing playing to mute.\n啥么都不在播放！")
        await mp.delete(k)
        await m.delete()
        return
    group_call.set_is_mute(True)
    k=await m.reply_text(f"{emoji.MUTED_SPEAKER} Muted\n已静音")
    await mp.delete(k)
    await m.delete()

@Client.on_message(filters.command(["unmute", f"unmute@{U}"]) & filters.user(ADMINS) & (filters.chat([CHAT,LOG_GROUP]) | filters.private))
async def unmute(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        k=await m.reply_text("Nothing playing to mute.\n啥么都不在播放！")
        await mp.delete(k)
        await m.delete()
        return
    group_call.set_is_mute(False)
    k=await m.reply_text(f"{emoji.SPEAKER_MEDIUM_VOLUME} Unmuted\n已取消静音")
    await mp.delete(k)
    await m.delete()

@Client.on_message(filters.command(["playlist", f"playlist@{U}"]) & (filters.chat([CHAT,LOG_GROUP]) | filters.private))
async def show_playlist(_, m: Message):
    if not playlist:
        k=await m.reply_text(f"{emoji.NO_ENTRY} No songs are playing\n啥么都不在播放！")
        await mp.delete(k)
        await m.delete()
        return
    else:
        pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
            f"**{i}**. **🎸{x[1]}**\n   👤**Requested by:** {x[4]}"
            for i, x in enumerate(playlist)
            ])
    if m.chat.type == "private":
        await m.reply_text(pl)
    else:
        if msg.get('playlist') is not None:
            await msg['playlist'].delete()
        msg['playlist'] = await m.reply_text(pl)
    await m.delete()

admincmds=[
    "join", "unmute", "mute", "leave", "clean", "vc", "pause", "resume", "stop", "skip", "radio", "stopradio", "replay", "restart",  "vol"
    f"join@{U}", f"unmute@{U}", f"mute@{U}", f"leave@{U}", f"clean@{U}", f"vc@{U}", f"pause@{U}", f"resume@{U}", f"stop@{U}", f"skip@{U}", 
    f"radio@{U}", f"stopradio@{U}", f"replay@{U}", f"restart@{U}", f"vol@{U}"]

@Client.on_message(filters.command(admincmds) & ~filters.user(ADMINS) & (filters.chat([CHAT,LOG_GROUP]) | filters.private))
async def notforu(_, m: Message):
    k=await m.reply("你想干啥？介要找管理员去干～")
    await mp.delete(k)
    await m.delete()

