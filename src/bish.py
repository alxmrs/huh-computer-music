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


@cli.resultcallback()
def rx_process_commands(processors):
    # start with generator
    stream = ()

    for proc in processors:
        stream = proc(stream)

    input('Press any key to stop\n')


@cli.command('period')
@click.option('-i', '--interval', type=int, default=999,
              help='How many milliseconds to wait before generating the next period')
@types.rx_generator
def metronome_cmd(stream, interval) -> rx.Observable:
    return (rx.Observable
            .interval(interval)
            )


@cli.command('ts')
@click.option('-r', '--sample-rate', type=int, default=8000, help='Number of samples per second (Hz).')
@types.processor
def ts_cmd(observable: rx.Observable, sample_rate: int) -> rx.Observable:
    return observable.map(lambda s: hcm.ts.time(s, s+1, sample_rate))


@cli.command('trace')
@types.processor
def trace_cmd(observable: rx.Observable) -> rx.Observable:
    """Writes input to stdout."""
    observable.subscribe(click.echo)
    return observable


if __name__ == '__main__':
    cli()
    input('Type any input to stop')