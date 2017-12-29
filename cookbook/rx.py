
import datetime as dt
# TODO(Alex) Fix imports, they are messy
from hcm.io import wav_write, append
from hcm.music.notes import notes
from hcm.music.keys import keys
from hcm.music.music import scale_constructor, \
    tempo_to_frequency, frequency_map

from hcm.signal.osc import sine, triangle

from hcm.ts import sample_and_hold

import hcm.signal

import rx

import numpy as np
import sounddevice as sd


PERIOD_SEC_LEN = 1
SAMPLE_RATE = 8000
BLOCK_SIZE = PERIOD_SEC_LEN * SAMPLE_RATE


# TODO(Alex) Break classes out into file/package
class AudioOutput(rx.Observer):

    def __init__(self):
        super().__init__()

        self.stream = sd.Stream(channels=1,
                                blocksize=BLOCK_SIZE,
                                samplerate=SAMPLE_RATE,
                                dtype=np.float32)

    def on_next(self, val):
        self.stream.write(val.T)

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

    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename
        self.cache = None

    def on_next(self, value):
        if self.cache is None:
            self.cache = value
        else:
            self.cache = append(self.cache, value)

    def on_completed(self):
        pass

    def write_wav(self):
        wav_write(self.filename, SAMPLE_RATE, self.cache)

    def on_error(self, error):
        print('An error occured, couldn\'t output wavefile', error)


if __name__ == '__main__':
    f0 = notes['Eb2']
    key = keys['Mixolydian']

    scale = scale_constructor(f0, key, 2)

    hold = tempo_to_frequency(200, 'quarter')

    ts = rx.Observable.interval(1000) \
        .map(lambda i: hcm.signal.time(i, i + 1, SAMPLE_RATE)) \

    control = ts \
        .map(lambda t: sine(t, f0)) \
        .map(lambda s: sample_and_hold(s, SAMPLE_RATE, hold)) \
        .map(lambda s: frequency_map(s, scale)) \

    period = rx.Observable.zip(ts, control,
                            lambda t, c: hcm.signal.VCO(t, c, sine))

    period.subscribe(print)

    output = AudioOutput()
    period.subscribe(output)
    output.start()

    # # Uncomment to write to file
    # wout = WavFileOutput('./cache1.wav')
    # period.subscribe(wout)
    # input('Press any key to stop')
    # wout.write_wav()

    input('Press any key to stop')
