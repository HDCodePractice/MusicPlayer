import asyncio
from typing import Callable
import av

class AudioFifo(av.AudioFifo):
    def __init__(self, BufferLimit: int = 5, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AUDIOBUFFERLIMITMS = BufferLimit * 50 * 960

        self.haveToFillBuffer = False

    def read(self, samples: int = 960) -> bytes:

        AudioFrame = super().read(samples)
        if not AudioFrame:
            return None

        if self.samples < self.AUDIOBUFFERLIMITMS:
            self.haveToFillBuffer = False
        else:
            self.haveToFillBuffer = True

        return AudioFrame

    def write(self, *args, **kwargs):
        super().write(*args, **kwargs)
        if self.samples < self.AUDIOBUFFERLIMITMS:
            self.haveToFillBuffer = False
        else:
            self.haveToFillBuffer = True

    def reset(self):
        # super().read(samples=max(self.samples - 960, 0), partial=True)
        super().read(0)

class AudioFileFifo():
    file = None
    result = None
    fifo = None
    resampler = None
    on_playout_end_call = None
    loop = None

    def __init__(self):
        self.fifo = AudioFifo()
        self.resampler = av.AudioResampler(format="s16", layout="stereo", rate=48000)
    
    def on_playout_ended(self,callback: Callable):
        if not asyncio.iscoroutinefunction(callback):
            raise RuntimeError('Sync callback does not supported')
        self.on_playout_end_call = callback
        return callback

    def on_played_data(self,gc, length):
        data = None
        if self.fifo:
            data = self.fifo.read(length / 4)
            if data:
                data = data.to_ndarray().tobytes()
            else:
                if self.fifo.samples > 0:
                    self.fifo.reset()
                    task = self.loop.create_task(self.on_playout_end_call())
        return data

    async def avdecode(self, file):
        self.file = file
        self.fifo = AudioFifo()
        self.fifo.reset()
        self.resampler = av.AudioResampler(format="s16", layout="stereo", rate=48000)
        await self._av_decode()

    async def _av_decode(self):
        self._input = av.open(self.file)
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
        self._input.close()
