
import datetime as dt
# TODO(Alex) Fix imports, they are messy

from hcm.dynamical import lorenz

from hcm.io import wav_write, append, add_channels
from hcm.music import notes, keys
from hcm.music import scale_constructor, \
    tempo_to_frequency, frequency_map

from hcm.signal.osc import sine, triangle


from hcm.ts import sample_and_hold

import hcm.signal

from rx import Observable, Observer

import numpy as np
import sounddevice as sd


PERIOD_SEC_LEN = 1
SAMPLE_RATE = 8000
BLOCK_SIZE = PERIOD_SEC_LEN * SAMPLE_RATE


# TODO(Alex) Break classes out into file/package
class AudioOutput(Observer):

    def __init__(self, channels=1):
        super().__init__()

        self.stream = sd.Stream(channels=channels,
                                blocksize=BLOCK_SIZE,
                                samplerate=SAMPLE_RATE,
                                dtype=np.float32)

    def on_next(self, val):
        self.stream.write(np.ascontiguousarray(val, dtype=np.float32))

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


class WavFileOutput(Observer):

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
        print(self.cache.shape)
        wav_write(self.filename, SAMPLE_RATE, self.cache)

    def on_error(self, error):
        print('An error occured, couldn\'t output wavefile', error)


def period_interval(ms_interval, duration_sec=1, sample_rate=SAMPLE_RATE):
    return Observable.interval(ms_interval) \
        .map(lambda i: hcm.signal.time(i * duration_sec,
                                       (i + 1) * duration_sec,
                                       sample_rate))


class WavPlotOutput(Observer):

    def __init__(self):
        super().__init__()

    def on_completed(self):
        pass

    def on_error(self, error):
        pass

    def on_next(self, value):
        pass


if __name__ == '__main__':
    f0 = notes['Db2']
    key = keys['Pentatonic']

    scale = scale_constructor(f0, key, 3)

    hold = tempo_to_frequency(300, 'quarter')

    ts = period_interval(999)

    control = ts \
        .map(lambda t: sine(t, f0)) \
        .map(lambda s: sample_and_hold(s, SAMPLE_RATE, hold)) \
        .map(lambda s: frequency_map(s, scale))

    control2 = ts \
        .map(lambda t: triangle(t, f0)) \
        .map(lambda s: sample_and_hold(s, SAMPLE_RATE, hold)) \
        .map(lambda s: frequency_map(s, scale))

    lor = ts \
        .map(lambda t: lorenz(t, 1))

    control3 = lor \
        .map(lambda tpl: sample_and_hold(tpl[0], SAMPLE_RATE, hold)) \
        .map(lambda s: frequency_map(s, scale))

    period = Observable.zip(ts, control,
                            lambda t, c: hcm.signal.VCO(t, c, sine))

    channel1 = period

    channel2 = Observable.zip(ts, control2,
                              lambda t, c: hcm.signal.VCO(t, c, triangle))

    channel3 = Observable.zip(ts, control3,
                              lambda t, c: hcm.signal.VCO(t, c, triangle))

    dual_channel = Observable.zip(channel1, channel2,
                                  lambda p1, p2: add_channels([p1, p2]))

    period.subscribe(print)

    output = AudioOutput(channels=2)
    dual_channel.subscribe(output)
    output.start()

    # Uncomment to write to file
    wout = WavFileOutput('./cache2.wav')
    dual_channel.subscribe(wout)
    input('Press any key to stop')
    wout.write_wav()

    input('Press any key to stop')
