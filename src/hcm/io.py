import numpy as np
import rx
import scipy
import scipy.io

import sounddevice as sd


PERIOD_SEC_LEN = 1
SAMPLE_RATE = 8000
BLOCK_SIZE = PERIOD_SEC_LEN * SAMPLE_RATE


def add_channels(signals):
    return np.array(np.vstack(signals)).T


def append(*signals):
    return np.array(np.hstack(signals))


def wav_read(filename):
    """Import .wav files from current directory. """
    return scipy.io.wavfile.read(filename)[1]


def wav_write(filename, sample_rate, file):
    """Export array to .wav file in current directory. """
    return scipy.io.wavfile.write(filename, sample_rate, file)


def sample_reader(filename):
    """Read in a sample (i.e. an audio snippet)"""
    sample = wav_read(filename)
    sample = np.true_divide(sample, max(sample))
    return sample


class AudioOutput(rx.Observer):

    def __init__(self,
                 channels=1,
                 sample_rate: int = SAMPLE_RATE,
                 period_length_sec: int = 1):
        super().__init__()

        block_size = period_length_sec * sample_rate

        self.stream = sd.Stream(channels=channels,
                                blocksize=block_size,
                                samplerate=sample_rate,
                                dtype=np.float32)

    def on_next(self, val):
        try:
            self.stream.write(np.ascontiguousarray(val, dtype=np.float32))
        except sd.PortAudioError:
            pass

    def on_error(self, err):
        self._close_stream()

    def on_completed(self):
        self._close_stream()

    def _close_stream(self):
        self.stream.close()

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()


class WavFileOutput(rx.Observer):

    def __init__(self, filename: str, sample_rate: int = 8000):
        super().__init__()
        self.filename = filename
        self.cache = None
        self.sample_rate = sample_rate

    def on_next(self, value):
        if self.cache is None:
            self.cache = value
        else:
            self.cache = np.append(self.cache, value, axis=0)
            # self.cache = append(self.cache, value)

    def on_completed(self):
        pass

    def write_wav(self):
        wav_write(self.filename, self.sample_rate, self.cache)

    def on_error(self, error):
        print('An error occured, couldn\'t output wavefile', error)
