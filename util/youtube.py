from youtube_dl import YoutubeDL
from os import path
import asyncio

def get_ydl():
    ydl_opts = {
        "geo-bypass": True,
        "nocheckcertificate": True
        }
    ydl = YoutubeDL(ydl_opts)
    return ydl

def get_finalurl(url):
    ydl = get_ydl()
    info = ydl.extract_info(url, download=False)
    return info["url"]

def get_first_finalurl(url):
    ydl = get_ydl()
    info = ydl.extract_info(url, download=False)
    return info["formats"][0]["url"]

def get_download_ydl():
    ydl_opts = {
        "format": "worstaudio[ext=m4a]",
        "geo-bypass": True,
        "nocheckcertificate": True,
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "continuedl" : True
    }
    ydl = YoutubeDL(ydl_opts)
    return ydl

async def youtube_downaudio(url: str) -> str:
    ydl = get_download_ydl()
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, ydl.download, [url])
    except Exception as e:
        print(e)
        return None
    return path.join("downloads", f"{info['id']}.{info['ext']}")

if __name__ == "__main__":
    # url = "https://www.youtube.com/watch?v=_daTfgc4u3k"
    # furl = get_first_finalurl(url)
    # print(furl)

    url = "https://www.youtube.com/watch?v=kYEC7bm7gFs"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(youtube_downaudio(url))

