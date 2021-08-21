#MIT License

#Copyright (c) 2021 SUBIN

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
from environs import Env
import re
from io import StringIO
from dotenv import load_dotenv

import requests
from base64 import b64encode

def get_doppler_env(token):
    token_b64 = b64encode(f"{token}:".encode()).decode()

    url = "https://api.doppler.com/v3/configs/config/secrets/download"

    querystring = {"format":"env"}

    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {token_b64}"
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            return response.text
    except Exception:
        pass
    return ""

env = Env()
env.read_env(f"{os.getcwd()}/local.env")

doppler_token = env.str('DOPPLER_TOKEN', default='')

if len(doppler_token) > 0 :
    response = get_doppler_env(doppler_token)
    if len(response) > 0:
        config = StringIO(response)
        load_dotenv(stream=config)

from youtube_dl import YoutubeDL
ydl_opts = {
    "geo-bypass": True,
    "nocheckcertificate": True
    }
ydl = YoutubeDL(ydl_opts)
links=[]
finalurl=""
finalurl=os.environ.get("STREAM_URL", "https://www.youtube.com/watch?v=rGPXugD0ekU")
# regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
# match = re.match(regex,STREAM)
# if match:
#     meta = ydl.extract_info(STREAM, download=False)
#     formats = meta.get('formats', [meta])
#     for f in formats:
#         links.append(f['url'])
#     finalurl=links[0]
# else:
#     finalurl=STREAM


class Config:
    WORKDIR=os.getcwd()
    ADMIN = os.environ.get("ADMINS", '')
    ADMINS = [int(admin) if re.search('^\d+$', admin) else admin for admin in (ADMIN).split()]
    API_ID = int(os.environ.get("API_ID", ''))
    CHAT = int(os.environ.get("CHAT", ""))
    LOG_GROUP=os.environ.get("LOG_GROUP", "")
    if LOG_GROUP:
        LOG_GROUP=int(LOG_GROUP)
    else:
        LOG_GROUP=None
    STREAM_URL=finalurl
    ADMIN_ONLY=os.environ.get("ADMIN_ONLY", "N")
    REPLY_MESSAGE=os.environ.get("REPLY_MESSAGE", None)
    if REPLY_MESSAGE:
        REPLY_MESSAGE=REPLY_MESSAGE
    else:
        REPLY_MESSAGE=None
    DURATION_LIMIT=int(os.environ.get("MAXIMUM_DURATION", 15))
    DELAY = int(os.environ.get("DELAY", 10))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 
    SESSION = os.environ.get("SESSION_STRING", "")
    playlist=[]
    msg = {}