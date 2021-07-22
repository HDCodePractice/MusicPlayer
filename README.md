# Telegram Voice Chat Bot with Channel Support.

A Telegram Bot to Play Audio in Voice Chats With Youtube and Deezer support.
Supports Live streaming from youtube

```
Please fork this repository don't import code
Made with Python3
(C) @subinps @老房东
Copyright permission under MIT License
License -> https://github.com/HDCodePractice/MusicPlayer/blob/master/LICENSE

```

## Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/HDCodePractice/MusicPlayer)

NOTE: Make sure you have started a VoiceChat in your Group before deploying.
### Deploy to VPS

```sh
git clone https://github.com/HDCodePractice/MusicPlayer
cd MusicPlayer
pip3 install -r requirements.txt
# <Create Variables appropriately>
python3 main.py
```

### 部署到Docker

Build Docker Image

```
docker build -t musicplayer:latest https://github.com/HDCodePractice/MusicPlayer.git#main
```

#### 测试容器的运行

```
docker run --name mpbot -v `pwd`:/data --env-file local.env -it musicplayer
```

这时会让你输入登录相关信息后，就可以运行了。


#### 启动和停止容器

一但容器运行正常后，你可以启动和停止容器

```
docker start mpbot
docker stop mpbot
docker restart mpbot
```

#### 查看运行中的容器

```
docker stats 
docker ps -a
```

#### 进入容器

```
docker exec -it mpbot /bin/bash
```

#### 删除容器

```
docker rm mpbot
```

#### 查看容器的日志

```
docker logs -f mpbot
```

### 使用dcoker-compose部署

```
git clone https://github.com/HDCodePractice/MusicPlayer.git
docker-compose build
```

新建一个 local.env 文件。运行初始化

```
docker-compose run mpbot
```

录入一下手机号和登录信息。

启动服务

```
docker-compose up -d
```

进入服务

```
docker-compose exec mpbot bash
```

停止服务

```
docker-compose stop
```

参考资料： [Docker Reference](https://docs.docker.com/reference/)

# Vars:
1. `API_ID` : Get From my.telegram.org
2. `API_HASH` : Get from my.telegram.org
3. `BOT_TOKEN` : @Botfather
4. `SESSION_STRING` : Generate From here [![GenerateStringName](https://img.shields.io/badge/repl.it-generateStringName-yellowgreen)](https://repl.it/@subinps/getStringName)
5. `CHAT` : ID of Channel/Group where the bot plays Music.
6. `LOG_GROUP` : Group to send Playlist, if CHAT is a Group
7. `ADMINS` : ID of users who can use admin commands.
8. `ARQ_API` : Get it for free from [@ARQRobot](https://telegram.dog/ARQRobot), This is required for /dplay to work.
9. `STREAM_URL` : Stream URL of radio station or a youtube live video to stream when the bot starts or with /radio command.
10. `MAXIMUM_DURATION` : Maximum duration of song to play.(Optional)
11. `REPLY_MESSAGE` : A reply to those who message the USER account in PM. Leave it blank if you do not need this feature. 
12. `ADMIN_ONLY` : Pass `Y` If you want to make /play and /dplay commands only for admins of `CHAT`. By default /play and /dplay is available for all.

- Enable the worker after deploy the project to Heroku
- Bot will starts radio automatically in given `CHAT` with given `STREAM_URL` after deploy.(24*7 Music even if heroku restarts, radio stream restarts automatically.)  
- To play a song use /play as a reply to audio file or a youtube link.
- Use /play <song name> to play song from youtube and /dplay <song name> to play from Deezer.
- Use /help to know about other commands.

**Features**

- Playlist, queue
- Supports Live streaming from youtube
- Supports both deezer and youtube to search songs.
- Play from telegram file supported.
- Starts Radio after if no songs in playlist.
- Automatically downloads audio for the first two tracks in the playlist to ensure smooth playing
- Automatic restart even if heroku restarts.

### Note

```
Contributions are welcomed, But Kanging and editing a few lines wont make you a Developer.
Fork the repo, Do not Import code.

```
#### Support

Connect Me On [Telegram](https://telegram.dog/subinps_bot)

## Credits 
- [Dash Eclipse's](https://github.com/dashezup) for his [tgvc-userbot](https://github.com/callsmusic/tgvc-userbot).

