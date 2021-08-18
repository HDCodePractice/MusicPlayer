# import threading
import av

class AudioFifo(av.AudioFifo):
    def __init__(self, BufferLimit: int = 5, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.AUDIOBUFFERLIMITMS = BufferLimit * 50 * 960

        # self.haveToFillBuffer = threading.Event()
        # self.haveToFillBuffer.set()

        self.haveToFillBuffer = False

    def read(self, samples: int = 960) -> bytes:

        AudioFrame = super().read(samples)
        if not AudioFrame:
            return None

        if self.samples < self.AUDIOBUFFERLIMITMS:
            # self.haveToFillBuffer.set()
            self.haveToFillBuffer = False
        else:
            # self.haveToFillBuffer.clear()
            self.haveToFillBuffer = True

        return AudioFrame

    def write(self, *args, **kwargs):
        super().write(*args, **kwargs)
        if self.samples < self.AUDIOBUFFERLIMITMS:
            # self.haveToFillBuffer.set()
            self.haveToFillBuffer = False
        else:
            # self.haveToFillBuffer.clear()
            self.haveToFillBuffer = True

    def reset(self):
        super().read(samples=max(self.samples - 960, 0), partial=True)