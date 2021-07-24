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
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton,Message
from pyrogram import Client, filters
import signal
from utils import USERNAME, FFMPEG_PROCESSES, mp
from config import Config
import os
import sys
U=USERNAME
CHAT=Config.CHAT
LOG_GROUP=Config.LOG_GROUP
msg=Config.msg
HOME_TEXT = "<b>Hello, [{}](tg://user?id={})\n\nI am HDMusicPlayer 1.0 which plays music in Channels and Groups 24/7.\n\nI can even Stream Youtube Live in Your Voicechat.\n\nHit /help to know about available commands.</b>\n==========================\n<b>你好，[{}](tg://user?id={})\n\n我是 HDMusicPlayer 1.0，它可以全天在频道和组中播放音乐。\n\n我甚至可以在你的语音聊天里放Youtube直播视频。\n\n点击 /help 了解可用命令。</b>"
HELP = """

<b>Use /play <song name> or use /play as a reply to an audio file or youtube link.

You can also use /dplay <song name> to play a song from Deezer.</b>

**Common Commands**:

**/play or /y**  Reply to an audio file or YouTube link to play it or use /play <song name>.
**/dplay** Play music from Deezer, Use /dplay <song name>
**/player**  Show current playing song.
**/help** Show help for commands
**/playlist** Shows the playlist.

**Admin Commands**:
**/skip** [n] ...  Skip current or n where n >= 2
**/join**  Join voice chat.
**/leave**  Leave current voice chat
**/vc**  Check which VC is joined.
**/stop**  Stop playing.
**/radio** Start Radio.
**/stopradio** Stops Radio Stream.
**/replay**  Play from the beginning.
**/clean** Remove unused RAW PCM files.
**/pause** Pause playing.
**/resume** Resume playing.
**/mute**  Mute in VC.
**/unmute**  Unmute in VC.
**/restart** Restarts the Bot.
=======================
<b>使用 /play <song name> 或使用 /play 作为对音频文件或 YouTube 链接的回复。

您还可以使用 /dplay <song name> 播放 Deezer 中的歌曲。</b>

**常用命令**：

**/play 或 /y** 回复音频文件或 YouTube 链接以播放它或使用 /play <歌曲名称>。
**/dplay** 从 Deezer 播放音乐，使用 /dplay <歌曲名称>
**/player** 显示当前播放的歌曲。
**/help** 显示命令帮助
**/playlist** 显示播放列表。

**管理命令**：
**/skip** [n] ... 跳过当前或 n，其中 n >= 2
**/join** 加入语音聊天。
**/leave** 离开当前语音聊天
**/vc** 检查加入的VC。
**/stop** 停止播放。
**/radio** 开始广播。
**/stopradio** 停止广播流。
**/replay** 从头开始播放。
**/clean** 删除未使用的 RAW PCM 文件。
**/pause** 暂停播放。
**/resume** 继续播放。
**/mute** 在 VC 中静音。
**/unmute** 在 VC 中取消静音。
**/restart** 重新启动机器人。
"""



@Client.on_message(filters.command(['start', f'start@{U}']))
async def start(client, message:Message):
    buttons = [
    [
        InlineKeyboardButton('👨🏼‍🦯 Help', callback_data='help'),
    ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    m=await message.reply(HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    await mp.delete(m)
    await message.delete()



@Client.on_message(filters.command(["help", f"help@{U}"]))
async def show_help(client, message:Message):
    buttons = [
        [
            InlineKeyboardButton('👨🏼‍💻 Developer', url='https://t.me/chstockbot'),
            InlineKeyboardButton('🧩 Source', url='https://github.com/HDCodePractice/MusicPlayer'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    if msg.get('help') is not None:
        await msg['help'].delete()
    msg['help'] = await message.reply_text(
        HELP
        )
    await message.delete()

@Client.on_message(filters.command(["restart", f"restart@{U}"]) & filters.user(Config.ADMINS) & (filters.chat([CHAT,LOG_GROUP]) | filters.private))
async def restart(client, message:Message):
    await message.reply_text("🔄 Restarting...")
    await message.delete()
    process = FFMPEG_PROCESSES.get(CHAT)
    if process:
        process.send_signal(signal.SIGTERM) 
    os.execl(sys.executable, sys.executable, *sys.argv)
    
