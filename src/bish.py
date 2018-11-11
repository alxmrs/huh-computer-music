import typing

import click
import rx

import hcm
import hcm.io
import hcm.music
import hcm.ts

from hcm import types
from hcm.signal import osc, vc

SAMPLE_RATE = 8000  # hz
INTERVAL_LENGTH = 1000  # ms

WAVES = {'sine': osc.sine, 'triangle': osc.triangle, 'square': osc.square}


@click.group(chain=True, cls=types.AliasedGroup)
def cli():
    """This script generates sounds via pipelined commands.

    Example:
        bish period trace ts osc scale-map vco mul -v 0.05 trace speaker

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

    input('Press any key to stop\n')


def first(it: typing.Iterable):
    """Gets the first value of an iterable"""
    return it.__iter__().__next__()


def identity(x):
    """The identity function: returns input unmodified."""
    return x


def handle_endofunctor(obv, op: typing.Callable = identity):
    """Performs input operation on the right value in the case of an endofunctor input or the raw value otherwise."""
    if type(obv) is tuple and len(obv) == 2:
        return obv[0], op(obv[1])
    else:
        return op(obv)


def parse_endofunctor(obs):
    """Returns either the right value in the case of an endofunctor or the raw value otherwise."""
    if type(obs) is tuple and len(obs) == 2:
        return obs[1]
    return obs


@cli.command('period')
@click.option('-i', '--interval', type=int, default=INTERVAL_LENGTH,
              help='How many milliseconds to wait before generating the next period')
@types.rx_generator
def period_cmd(stream, interval) -> rx.Observable:
    """Count up from zero on a timed interval."""
    return rx.Observable.interval(interval - 1)


@cli.command('time-series')
@click.option('-r', '--sample-rate', type=int, default=SAMPLE_RATE, help='Number of samples per second (Hz).')
@types.processor
def ts_cmd(observable: rx.Observable, sample_rate: int) -> rx.Observable:
    """Transform an integer into a 1 second time-series with the desired sample rate."""
    global SAMPLE_RATE
    SAMPLE_RATE = sample_rate
    end_range = INTERVAL_LENGTH / 1000
    return observable.map(lambda s: hcm.ts.time(s, s + end_range, sample_rate))


@cli.command('trace')
@types.processor
def trace_cmd(observable: rx.Observable) -> rx.Observable:
    """Writes input to stdout."""
    observable.subscribe(click.echo)
    return observable


@cli.command('speaker')
@click.option('-c', '--channels', type=int, default=2, help='Number of output channels')
@types.processor
def speaker_cmd(observable: rx.Observable, channels: int) -> rx.Observable:
    """Pipes input audio stream to speaker"""

    speaker_observer = hcm.io.AudioOutput(channels=channels)

    (
        observable
        .map(parse_endofunctor)
        .subscribe(speaker_observer)
    )

    speaker_observer.start()

    return observable


@cli.command('oscillate')
@click.option('-w', '--wave', type=click.Choice(list(WAVES.keys())), default=first(WAVES.keys()))
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
@click.option('-c', '--constant', type=float, default=0)
@types.processor
def mult_cmd(observable: rx.Observable, constant) -> rx.Observable:
    """Multiply the input signal by a constant"""
    def handle_mul(obv):
        return handle_endofunctor(obv, lambda o: constant * o)

    return observable.map(handle_mul)


@cli.command('quantize-frequency')
@click.option('-b', '--bpm', type=int, default=150)
@click.option('-d', '--note-duration',
              type=click.Choice(list(hcm.music.DURATIONS.keys())),
              default=first(hcm.music.DURATIONS.keys()))
@types.processor
def quantize_cmd(observable: rx.Observable, bpm: int = 150, note_duration: str = 'quarter') -> rx.Observable:
    """Quantize input frequency given a desired beats-per-minute and note duration."""
    hold = hcm.music.tempo_to_frequency(bpm, note_duration)
    return observable.map(lambda o: (o[0], hcm.ts.sample_and_hold(o[1], SAMPLE_RATE, hold)))


@cli.command('scale-map')
@click.option('-f', '--freq-start', type=float, default=261.63)
@click.option('-k', '--key', type=click.Choice(list(hcm.music.keys.keys())), default=first(hcm.music.keys.keys()))
@click.option('-n', '--num-octaves', type=int, default=2)
@types.processor
def scale_map_cmd(observable: rx.Observable, freq_start, key: str, num_octaves: int = 2) -> rx.Observable:
    """Map input control signal into a musical scale with a starting frequency, key, and octave range."""
    chosen_key = hcm.music.keys[key]
    scale = hcm.music.scale_constructor(freq_start, chosen_key, num_octaves)
    return observable.map(lambda o: (o[0], hcm.music.frequency_map(o[1], scale)))


@cli.command('voltage-controlled-oscillator')
@click.option('-w', '--wave', type=click.Choice(list(WAVES.keys())), default=first(WAVES.keys()))
@types.processor
def vco_cmd(observable: rx.Observable, wave) -> rx.Observable:
    """Use the input as a control signal for frequency.

    Can specify the type of oscillation (sine, triangle, square waves)

    Args:
        observable: Observable with input signal. Should be a tuple with the input time-series and control signal.
        wave: Type of oscillator (Choice of sine, triangle, or square waves).

    Returns:
        A single time series representing the new audio.

    """
    chosen_wave = WAVES[wave]
    return observable.map(lambda o: vc.VCO(*o, chosen_wave))


if __name__ == '__main__':
    cli()
