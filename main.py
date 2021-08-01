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
from pyrogram import Client, idle
import os
from config import Config
from utils import mp
from pyrogram.raw import functions, types

CHAT=Config.CHAT
bot = Client(
    "Musicplayer",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workdir=Config.WORKDIR,
    plugins=dict(root="plugins",
        include=[
        "callback",
        "commands",
        "inline",
        "player",
        "radio"
        ])
)
if not os.path.isdir("./downloads"):
    os.makedirs("./downloads")
async def main():
    async with bot:
        await mp.start_radio()

bot.run(main())
bot.start()
bot.send(
    functions.bots.SetBotCommands(
        commands=[
            types.BotCommand(
                command="start",
                description="Check if bot alive//看一看机器人还是不是活着的"
            ),
            types.BotCommand(
                command="help",
                description="Show the help message//显示帮助信息"
            ),
            types.BotCommand(
                command="play",
                description="Play a song. Syntax: /play <song name> //请用 /play 歌曲名 来点播歌曲"
            ),
            types.BotCommand(
                command="player",
                description="Shows current playing song with controls//查看正在播放的歌曲"
            ),
            types.BotCommand(
                command="playlist",
                description="Shows the playlist//查看playlist"
            ),
            types.BotCommand(
                command="skip",
                description="Skip the current song (reserved for admin)//跳过当前的歌曲（管理员专用）"
            ),
            types.BotCommand(
                command="join",
                description="Join VC (reserved for admin)//让我加入voice chat（管理员专用）"
            ),
            types.BotCommand(
                command="leave",
                description="Leave from VC (reserved for admin)//让我离开voice chat（管理员专用）"
            ),
            # types.BotCommand(
            #     command="vc",
            #     description="Check if VC is joined (reserved for admin)（管理员专用）"
            # ),
            types.BotCommand(
                command="stop",
                description="Stops Playing (reserved for admin)//停止播放（管理员专用）"
            ),
            types.BotCommand(
                command="radio",
                description="Start radio/Live stream (reserved for admin)//开启收音机/直播（管理员专用）"
            ),
            types.BotCommand(
                command="stopradio",
                description="Stops radio/Livestream (reserved for admin)//停止收音机/直播（管理员专用）"
            ),
            types.BotCommand(
                command="replay",
                description="Replay from beginning (reserved for admin)//重新开始播放playlist（管理员专用）"
            ),
            types.BotCommand(
                command="clean",
                description="Cleans RAW files (reserved for admin)//清除缓存文件(管理员专用)"
            ),
            types.BotCommand(
                command="pause",
                description="Pause the song (reserved for admin)//暂停歌曲（管理员专用）"
            ),
            types.BotCommand(
                command="resume",
                description="Resume the paused song (reserved for admin)//重新开始放歌曲（管理员专用）"
            ),
            # types.BotCommand(
            #     command="mute",
            #     description="Mute in VC (reserved for admin)//静音（管理员专用）"
            # ),
            # types.BotCommand(
            #     command="unmute",
            #     description="Unmute in VC (reserved for admin)//取消静音（管理员专用）"
            # ),
            types.BotCommand(
                command="restart",
                description="Restart the bot (reserved for admin)//从起机器人（管理员专用）"
            ),
            # types.BotCommand(
            #     command="vol",
            #     description="Change volume (reserved for admin)//变更音量（管理员专用）"
            # )
        ]
    )
)

idle()
bot.stop()
