import typing
import time

import numpy as np
import click

import rx
import hcm
import hcm.ts
import hcm.io
import hcm.music
from hcm.signal import osc, vc
from hcm import types

SAMPLE_RATE = 8000
INTERVAL_LENGTH = 1000

WAVES = {'sine': osc.sine, 'triangle': osc.triangle, 'square': osc.square}


@click.group(chain=True)
def cli():
    """This script processes textfiles through the nltk and similar packages in a unix pipe.
     One commands feeds into the next.

    Example:
        TBD

    """
    pass


@cli.resultcallback()
def rx_process_commands(processors):
    # start with generator
    stream = ()

    for proc in processors:
        stream = proc(stream)

    input('Press any key to stop\n')


def first(it: typing.Iterable):
    return it.__iter__().__next__()


def parse_endofunctor(obs):
    if type(obs) is tuple and len(obs) == 2:
        return obs[1]
    return obs


def identity(x):
    return x


def handle_endofunctor(obv, op: typing.Callable = identity):
    if type(obv) is tuple and len(obv) == 2:
        return obv[0], op(obv[1])
    else:
        return op(obv)


@cli.command('period')
@click.option('-i', '--interval', type=int, default=INTERVAL_LENGTH,
              help='How many milliseconds to wait before generating the next period')
@types.rx_generator
def metronome_cmd(stream, interval) -> rx.Observable:
    return rx.Observable.interval(interval - 1)


@cli.command('ts')
@click.option('-r', '--sample-rate', type=int, default=SAMPLE_RATE, help='Number of samples per second (Hz).')
@types.processor
def ts_cmd(observable: rx.Observable, sample_rate: int) -> rx.Observable:
    global SAMPLE_RATE
    SAMPLE_RATE = sample_rate
    return observable.map(lambda s: hcm.ts.time(s, s + 1, sample_rate))


@cli.command('trace')
@types.processor
def trace_cmd(observable: rx.Observable) -> rx.Observable:
    """Writes input to stdout."""
    observable.subscribe(click.echo)
    return observable


@cli.command('speaker')
@types.processor
def speaker_cmd(observable: rx.Observable) -> rx.Observable:
    """Pipes current audio stream to speaker (audio output)"""

    speaker_observer = hcm.io.AudioOutput(channels=2)

    (
        observable
            .map(parse_endofunctor)
            .subscribe(speaker_observer)
    )

    speaker_observer.start()
    return observable


@cli.command('osc')
@click.option('-w', '--wave', type=click.Choice(list(WAVES.keys())), default=first(WAVES.keys()))
@click.option('-f', '--frequency', type=float, default=1.0)
@types.processor
def osc_cmd(observable: rx.Observable, wave, frequency) -> rx.Observable:
    chosen_wave = WAVES[wave]

    return observable.map(lambda o: (o, chosen_wave(o, frequency)))


@cli.command('add')
@click.option('-v', '--val', type=float, default=0)
@types.processor
def osc_cmd(observable: rx.Observable, val) -> rx.Observable:
    def handle_add(obv):
        return handle_endofunctor(obv, lambda o: val + o)

    return observable.map(handle_add)


@cli.command('mul')
@click.option('-v', '--val', type=float, default=0)
@types.processor
def osc_cmd(observable: rx.Observable, val) -> rx.Observable:

    def handle_mul(obv):
        return handle_endofunctor(obv, lambda o: val * o)

    return observable.map(handle_mul)


@cli.command('quantize')
@click.option('-b', '--bpm', type=int, default=150)
@click.option('-d', '--note-duration',
              type=click.Choice(list(hcm.music.DURATIONS.keys())),
              default=first(hcm.music.DURATIONS.keys()))
@types.processor
def quantize_cmd(observable: rx.Observable, bpm: int = 150, note_duration: str = 'quarter') -> rx.Observable:
    hold = hcm.music.tempo_to_frequency(bpm, note_duration)
    return observable.map(lambda o: (o[0], hcm.music.sample_and_hold(o[1], SAMPLE_RATE, hold)))


@cli.command('scale-map')
@click.option('-f', '--freq-start', type=float, default=261.63)
@click.option('-k', '--key', type=click.Choice(list(hcm.music.keys.keys())), default=first(hcm.music.keys.keys()))
@click.option('-n', '--num-octaves', type=int, default=2)
@types.processor
def scale_map_cmd(observable: rx.Observable, freq_start, key: str, num_octaves: int = 2) -> rx.Observable:
    chosen_key = hcm.music.keys[key]
    scale = hcm.music.scale_constructor(freq_start, chosen_key, num_octaves)
    return observable.map(lambda o: (o[0], hcm.music.frequency_map(o[1], scale)))


@cli.command('vco')
@click.option('-w', '--wave', type=click.Choice(list(WAVES.keys())), default=first(WAVES.keys()))
@types.processor
def vco_cmd(observable: rx.Observable, wave) -> rx.Observable:
    chosen_wave = WAVES[wave]

    return observable.map(lambda o: vc.VCO(*o, chosen_wave))


if __name__ == '__main__':
    cli()
