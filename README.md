# Telegram 音乐点播收藏 Bot

A Telegram Bot to Play Audio in Voice Chats With Youtube support.
Supports Live streaming from youtube

```
Please fork this repository don't import code
Made with Python3
(C) @subinps @老房东 @Sichengthebest
Copyright permission under MIT License
License -> https://github.com/HDCodePractice/MusicPlayer/blob/master/LICENSE

```

## 部署到Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/HDCodePractice/MusicPlayer)

NOTE: Make sure you have started a VoiceChat in your Group before deploying.

### 部署到VPS

```sh
git clone https://github.com/HDCodePractice/MusicPlayer
cd MusicPlayer
pip3 install -r requirements.txt
# <Create Variables appropriately>
python3 main.py
```

### 部署到Docker

准备一个docker-compose.yml，可以参照[这里的示例](https://github.com/HDCodePractice/MusicPlayer/blob/main/docker-compose.yml)。

第一次运行时如果你的env文件里设置的是`SESSION_STRING=session`，需要手动运行一次进行telegram验证：

```
docker-compose run --rm mpbot
```

录入手机号和相关的密码后，看看运行是否正常，如果正常可以`ctrl+c`退出。

后台启动：

```
docker-compose up -d
```

服务停止：

```
docker-compose down
```


# 环境变量(参考[expmple_env](https://github.com/HDCodePractice/MusicPlayer/blob/main/example_env)):
1. `API_ID` : Get From my.telegram.org
2. `API_HASH` : Get from my.telegram.org
3. `BOT_TOKEN` : @Botfather
4. `SESSION_STRING` : 可以写一个string手工输入，也可以使用这里 [![GenerateStringName](https://img.shields.io/badge/repl.it-generateStringName-yellowgreen)](https://repl.it/@subinps/getStringName)来生成一个SESSION_STRING
5. `CHAT` : 播放音乐的群组ID
6. `LOG_GROUP` : 发送播放日志和Playlist的群组ID
7. `ADMINS` : 可以使用admin命令的用户ID，使用空格分割多个用户ID
8. `STREAM_URL` : Stream URL of radio station or a youtube live video to stream when the bot starts or with /radio command.
9. `MAXIMUM_DURATION` : Maximum duration of song to play.(Optional)
10. `REPLY_MESSAGE` : A reply to those who message the USER account in PM. Leave it blank if you do not need this feature. 
11. `ADMIN_ONLY` : Pass `Y` If you want to make /play  commands only for admins of `CHAT`. By default /play and /dplay is available for all.

- Enable the worker after deploy the project to Heroku
- Bot will starts radio automatically in given `CHAT` with given `STREAM_URL` after deploy.(24*7 Music even if heroku restarts, radio stream restarts automatically.)  
- To play a song use /play as a reply to audio file or a youtube link.
- Use /play <song name> to play song from youtube.
- Use /help to know about other commands.

**Features**

- Playlist, queue
- Supports Live streaming from youtube
- Supports youtube to search songs.
- Play from telegram file supported.
- Starts Radio after if no songs in playlist.
- Automatically downloads audio for the first two tracks in the playlist to ensure smooth playing
- Automatic restart even if heroku restarts.
- 支持使用bot来收藏歌曲
- 支持一键再次点播



