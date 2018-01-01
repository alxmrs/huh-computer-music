
import datetime as dt
import hcm.io
import hcm.ts
import hcm.music

# TODO(Alex) Figure out better module organization for this
from hcm.music.music import scale_constructor, tempo_to_frequency, frequency_map

import hcm.signal.osc as osc
import hcm.signal.vc as vc

import hcm.signal

import rx
import typing
import pathlib
import json

import numpy as np
import sounddevice as sd


PERIOD_SEC_LEN = 1
SAMPLE_RATE = 8000
BLOCK_SIZE = PERIOD_SEC_LEN * SAMPLE_RATE


# TODO(Alex) Break classes out into file/package
class AudioOutput(rx.Observer):

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


class WavFileOutput(rx.Observer):

    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename
        self.cache = None

    def on_next(self, value):
        if self.cache is None:
            self.cache = value
        else:
            self.cache = hcm.io.append(self.cache, value)

    def on_completed(self):
        pass

    def write_wav(self):
        hcm.io.wav_write(self.filename, SAMPLE_RATE, self.cache)

    def on_error(self, error):
        print('An error occured, couldn\'t output wavefile', error)


def read_config_file(filepath: typing.Union[pathlib.Path, typing.AnyStr]) -> typing.Dict:
        with open(filepath) as json_file:
            return json.load(json_file)


def demo_control(ts, func, *, hold, scale):
    return ts \
        .map(func) \
        .map(lambda s: hcm.ts.sample_and_hold(s, SAMPLE_RATE, hold)) \
        .map(lambda sp: frequency_map(sp, scale=scale))


if __name__ == '__main__':

    config = read_config_file('cookbook/params.json')

    ctrl_hz = config['control_hertz']

    f0 = hcm.music.notes[config['start_note']]
    key = hcm.music.keys[config['key']]

    scale = scale_constructor(f0, key, config['num_octaves'])

    hold = tempo_to_frequency(config['tempo'], config['note_duration'])

    ts = rx.Observable.interval(1000) \
        .map(lambda i: hcm.ts.time(i, i + 1, SAMPLE_RATE)) \

    sine_control = demo_control(ts, lambda t: osc.sine(t, ctrl_hz),
                                hold=hold, scale=scale)

    triangle_control = demo_control(ts, lambda t: osc.triangle(t, ctrl_hz),
                                hold=hold, scale=scale)

    vco_sine = rx.Observable.zip(ts, sine_control,
                                 lambda t, c: vc.VCO(t, c, osc.sine))

    vco_triangle = rx.Observable.zip(ts, triangle_control,
                                     lambda t, c: vc.VCO(t, c, osc.triangle))

    vco_sine.subscribe(lambda x: print('sine: ', x.shape))
    vco_triangle.subscribe(lambda x: print('triangle: ', x.shape))

    dual_channel = rx.Observable.zip(vco_sine, vco_triangle,
                                     lambda s, t: hcm.io.add_channels([s, t]))

    output = AudioOutput(channels=2)
    dual_channel.subscribe(output)
    output.start()

    # # Uncomment to write to file
    # wout = WavFileOutput('./cache1.wav')
    # period.subscribe(wout)
    # input('Press any key to stop')
    # wout.write_wav()

    input('Press any key to stop')
