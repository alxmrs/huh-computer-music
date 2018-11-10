import hcm
import hcm.io
import hcm.music.const
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

PERIOD_SEC_LEN = 1
SAMPLE_RATE = 8000
BLOCK_SIZE = PERIOD_SEC_LEN * SAMPLE_RATE


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

    f0 = hcm.music.const.notes[config['start_note']]
    key = hcm.music.const.keys[config['key']]

    scale = scale_constructor(f0, key, config['num_octaves'])

    hold = tempo_to_frequency(config['tempo'], config['note_duration'])

    ts = rx.Observable.interval(990) \
        .map(lambda i: hcm.ts.time(i, i + 1, SAMPLE_RATE)) \


    def wavvy_control(osc_func):

        def func(t):
            return osc_func(np.exp(3 * np.sin(t)), ctrl_hz)

        return func


    sine_control = demo_control(ts, wavvy_control(osc.sine),
                                hold=hold, scale=scale)

    triangle_control = demo_control(ts, wavvy_control(osc.triangle),
                                hold=hold, scale=scale)

    vco_sine = rx.Observable.zip(ts, sine_control,
                                 lambda t, c: vc.VCO(t, c, osc.sine))

    vco_triangle = rx.Observable.zip(ts, triangle_control,
                                     lambda t, c: vc.VCO(t, c, osc.triangle))

    adsr_dur = 1 / hold
    quarter_dur = adsr_dur / 4
    adsr = vc.ADSR(quarter_dur, quarter_dur, 0.5, quarter_dur, duration=adsr_dur, sample_rate=SAMPLE_RATE)

    vca_sine = vco_sine.map(lambda x: vc.VCA(x, np.tile(adsr, len(x) // len(adsr) + 1)[:len(x)]))

    vca_triangle = vco_triangle.map(lambda x: vc.VCA(x, np.tile(adsr, len(x) // len(adsr) + 1)[:len(x)]))



    vca_sine.subscribe(lambda x: print('sine: ', x.shape))
    vca_triangle.subscribe(lambda x: print('triangle: ', x.shape))

    dual_channel = rx.Observable.zip(vca_sine, vca_triangle,
                                     lambda s, t: hcm.io.add_channels([s, t]))

    output = hcm.io.AudioOutput(channels=2)
    dual_channel.subscribe(output)
    output.start()

    # Uncomment to write to file
    wout = hcm.io.WavFileOutput('./wavvyadsr.wav')
    dual_channel.subscribe(wout)
    input('Press any key to stop')
    wout.write_wav()

    input('Press any key to stop')
