import asyncio
import concurrent.futures

import av
from .AudioFifo import AudioFifo

class AudioFileFifo():
    file = None
    result = None
    fifo = None
    resampler = None

    def __init__(self):
        self.fifo = AudioFifo()
        self.resampler = av.AudioResampler(format="s16", layout="stereo", rate=48000)

    def on_played_data(self,gc, length):
        data = None
        if self.fifo:
            data = self.fifo.read(length / 4)
            if data:
                data = data.to_ndarray().tobytes()
        return data

    async def avdecode(self, file):
        self.file = file
        self.fifo = AudioFifo()
        self.resampler = av.AudioResampler(format="s16", layout="stereo", rate=48000)
        await self._av_decode()

    async def _av_decode(self):
        self._input = av.open(self.file)
        count = 0
        for frame in self._input.decode():
            if frame:
                frame.pts = None
                frame = self.resampler.resample(frame)
                try:
                    while self.fifo.haveToFillBuffer:
                        await asyncio.sleep(0.01)
                except asyncio.CancelledError:
                    self._input.close()
                    self.fifo.reset()
                    raise
                self.fifo.write(frame)
                count += 1
        self._input.close()
