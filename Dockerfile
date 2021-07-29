FROM debian:latest

RUN apt update && apt upgrade -y
RUN apt install git curl python3-pip ffmpeg -y
# RUN pip3 install -U pip
RUN cd /
# RUN git clone https://github.com/HDCodePractice/MusicPlayer.git
COPY . /MusicPlayer/
RUN cd MusicPlayer
WORKDIR /MusicPlayer
RUN pip3 install -U -r requirements.txt
WORKDIR /data
CMD python3 /MusicPlayer/main.py