FROM python:latest

RUN apt-get update && apt upgrade -y && apt-get install -y curl ffmpeg libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libswresample-dev libavfilter-dev
RUN cd /
COPY . /MusicPlayer/
RUN cd MusicPlayer
WORKDIR /MusicPlayer
RUN pip3 install -r requirements.txt
WORKDIR /data
CMD python3 /MusicPlayer/main.py