FROM python:3.9.6-buster

RUN apt-get update && apt upgrade -y
RUN apt-get install git curl ffmpeg -y
RUN cd /
COPY . /MusicPlayer/
RUN cd MusicPlayer
WORKDIR /MusicPlayer
RUN pip3 install -U -r requirements.txt
WORKDIR /data
CMD python3 /MusicPlayer/main.py