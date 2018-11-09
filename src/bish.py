import typing
import time

import numpy as np
import click

import rx
import hcm
import hcm.ts
from hcm import types


@click.group(chain=True)
def cli():
    """This script processes textfiles through the nltk and similar packages in a unix pipe.
     One commands feeds into the next.

    Example:
        TBD

    """
    pass


@cli.resultcallback()
def process_commands(processors):
    """This result callback is invoked with an iterable of all the chained
    subcommands.  As in this example each subcommand returns a function
    we can chain them together to feed one into the other, similar to how
    a pipe on unix works.
    """
    # Start with an empty iterable.
    stream = ()

    # Pipe it through all stream processors.
    for processor in processors:
        stream = processor(stream)

    # Evaluate the stream and throw away the items.
    for _ in stream:
        pass


@cli.command('period')
@click.option('-i', '--interval', type=int, default=1000,
              help='How many milliseconds to wait before generating the next period')
@types.generator
def metronome_cmd(interval) -> typing.Iterable[int]:
    interval_sec = (interval - 5) / 1000
    target = time.time() + interval_sec
    i = 0
    while True:
        if time.time() >= target:
            target = time.time() + interval_sec
            yield i
            i += 1


@cli.command('ts')
@click.option('-r', '--sample-rate', type=int, default=8000, help='Number of samples per second (Hz).')
@types.processor
def ts_cmd(signals: typing.Iterable[int], sample_rate: int) -> typing.Iterable[np.ndarray]:
    for s in signals:
        yield hcm.ts.time(s, s+1, sample_rate)


@cli.command('trace')
@types.processor
def trace_cmd(signals: typing.Iterator) -> typing.Iterator:
    """Writes input to stdout."""
    for obs in signals:
        click.echo(obs)
        yield obs


if __name__ == '__main__':
    cli()