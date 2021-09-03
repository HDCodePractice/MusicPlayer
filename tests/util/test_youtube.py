import pytest
import asyncio
import time
import os

@pytest.mark.asyncio
async def test_youtube_downaudio():
    from util.youtube import youtube_downaudio
    before = time.monotonic()
    file = await youtube_downaudio("https://www.youtube.com/watch?v=kYEC7bm7gFs")
    after = time.monotonic()
    assert file == "downloads/kYEC7bm7gFs.m4a"
    assert after - before > 1
    fsize = os.path.getsize(file)
    assert fsize == 366883

def test_get_first_finalurl():
    from util.youtube import get_first_finalurl
    url = get_first_finalurl("https://www.youtube.com/watch?v=kYEC7bm7gFs")
    assert "https://manifest.googlevideo.com/api/manifest/dash/expire" in url 
    assert len(url) > 800

# def test_get_finalurl():
#     from util.youtube import get_finalurl
#     url = get_finalurl("https://www.youtube.com/watch?v=kYEC7bm7gFs")
#     assert "https://manifest.googlevideo.com/api/manifest/dash/expire" == url 
#     assert len(url) > 800