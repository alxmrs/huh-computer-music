#!/usr/bin/env python3

import typing

import click
import rx

import hcm
from hcm import types

SAMPLE_RATE = 8000  # hz
INTERVAL_LENGTH = 1000  # ms

WAVES = {'sine': hcm.sine_wave, 'triangle': hcm.sawtooth_wave, 'square': hcm.square_wave}


# TODO(#13)
@click.group(chain=True, cls=types.AliasedGroup)
def cli():
    """This script generates sounds via pipelined commands.

    The following examples demonstrate verbose and abbreviated
    usages of the CLI.

    Run these examples with caution regarding volume! Make sure you don't
    blow out your speakers.

    $ bin/bish period time-series oscillate scale-map vco multiply speaker

    $ bin/bish p ts osc sm vco mul sp
    """
    pass


@cli.resultcallback()
def rx_process_commands(processors):
    """Combine series of commands in unix-like pipe.

    Will run the pattern generated from the commands until a key is pressed.

    Args:
        processors: Commands produced from the Click CLI.
    """

    stream = ()

    for proc in processors:
        stream = proc(stream)

    input('Press enter to stop\n')
    print('Goodbye.')


def first(it: typing.Iterable):
    """Gets the first value of an iterable"""
    return it.__iter__().__next__()


def identity(x):
    """The identity function: returns input unmodified."""
    return x


def handle_endofunctor(obv, op: typing.Callable = identity):
    """Glue to handle 2-tuple valued returns."""
    if type(obv) is tuple and len(obv) == 2:
        return obv[0], op(obv[1])
    else:
        return op(obv)


def parse_endofunctor(obs):
    """Glue to parse 2-tuple values objects."""
    if type(obs) is tuple and len(obs) == 2:
        return obs[1]
    return obs


@cli.command('period')
@click.option('-i', '--interval',
              type=int,
              default=INTERVAL_LENGTH,
              help='Generate the next period in how many milliseconds?')
@types.rx_generator
def period_cmd(stream, interval) -> rx.Observable:
    """Count up from zero on a timed interval."""
    return rx.Observable.interval(interval - 1)


@cli.command('time-series')
@click.option('-r', '--sample-rate',
              type=int,
              default=SAMPLE_RATE,
              help='Number of samples per second (Hz).')
@types.processor
def ts_cmd(observable: rx.Observable, sample_rate: int) -> rx.Observable:
    """Transform an integer into a 1 second time-series."""
    global SAMPLE_RATE
    SAMPLE_RATE = sample_rate
    end_range = int(INTERVAL_LENGTH / 1000)
    return observable.map(lambda s: hcm.time(s, s + end_range, sample_rate))


@cli.command('trace')
@types.processor
def trace_cmd(observable: rx.Observable) -> rx.Observable:
    """Writes input to stdout."""
    observable.subscribe(click.echo)
    return observable


@cli.command('speaker')
@click.option('-c', '--channels',
              type=int,
              default=1,
              help='Number of output channels')
@types.processor
def speaker_cmd(observable: rx.Observable, channels: int) -> rx.Observable:
    """Pipes input audio stream to speaker"""

    speaker_observer = hcm.io.AudioOutput(channels=channels)

    observable \
        .map(parse_endofunctor) \
        .subscribe(speaker_observer)

    speaker_observer.start()

    return observable


@cli.command('oscillate')
@click.option('-w', '--wave',
              type=click.Choice(list(WAVES.keys())),
              default=first(WAVES.keys()))
@click.option('-f', '--frequency', type=float, default=1.0)
@types.processor
def osc_cmd(observable: rx.Observable, wave, frequency) -> rx.Observable:
    """Emit a sine, triangle, or square wave oscillation"""
    chosen_wave = WAVES[wave]
    return observable.map(lambda o: (o, chosen_wave(o, frequency)))


@cli.command('add')
@click.option('-c', '--constant', type=float, default=0)
@types.processor
def add_cmd(observable: rx.Observable, constant) -> rx.Observable:
    """Add a constant to the input signal"""

    def handle_add(obv):
        return handle_endofunctor(obv, lambda o: constant + o)

    return observable.map(handle_add)


@cli.command('multiply')
@click.option('-c', '--constant', type=float, default=1)
@types.processor
def mult_cmd(observable: rx.Observable, constant) -> rx.Observable:
    """Multiply the input signal by a constant"""

    def handle_mul(obv):
        return handle_endofunctor(obv, lambda o: constant * o)

    return observable.map(handle_mul)


@cli.command('quantize-frequency')
@click.option('-b', '--bpm', type=int, default=150)
@click.option('-d', '--note-duration',
              type=click.Choice(list(hcm.DURATIONS.keys())),
              default=first(hcm.DURATIONS.keys()))
@types.processor
def quantize_cmd(observable: rx.Observable,
                 bpm: int = 150,
                 note_duration: str = 'quarter') -> rx.Observable:
    """Quantize input frequency."""
    hold = hcm.tempo_to_frequency(bpm, note_duration)
    return observable.map(
        lambda o: (o[0], hcm.sample_and_hold(o[1], SAMPLE_RATE, hold))
    )


@cli.command('scale-map')
@click.option('-f', '--freq-start', type=float, default=261.63)
@click.option('-k', '--key',
              type=click.Choice(list(hcm.KEYS.keys())),
              default=first(hcm.KEYS.keys()))
@click.option('-n', '--num-octaves', type=int, default=2)
@types.processor
def scale_map_cmd(observable: rx.Observable,
                  freq_start,
                  key: str,
                  num_octaves: int = 2) -> rx.Observable:
    """Map input control signal into a musical scale."""
    chosen_key = hcm.KEYS[key]
    scale = hcm.scale_constructor(freq_start, chosen_key, num_octaves)
    return observable.map(
        lambda o: (o[0], hcm.frequency_map(o[1], scale))
    )


@cli.command('voltage-controlled-oscillator')
@click.option('-w', '--wave',
              type=click.Choice(list(WAVES.keys())),
              default=first(WAVES.keys()))
@types.processor
def vco_cmd(observable: rx.Observable, wave) -> rx.Observable:
    """Use the input as a control signal for frequency.

    Can specify the type of oscillation (sine, triangle, square waves)

    Args:
        observable: Observable with input signal. Should be a tuple with
            the input time-series and control signal.
        wave: Type of oscillator (Choice of sine, triangle, or square
            waves).

    Returns:
        A single time series representing the new audio.
    """
    chosen_wave = WAVES[wave]
    return observable.map(lambda o: hcm.VCO(*o, chosen_wave))


if __name__ == '__main__':
    cli()
