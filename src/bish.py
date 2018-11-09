import typing

import click

import rx
import hcm
from hcm import types
import threading

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

@cli.command('ts')
@click.option('-r', '--sample-rate', type=int, default=8000, help='Number of samples per second (Hz).')
@click.option('-i', '--interval', type=int, default=1000,
              help='How many milliseconds to wait before generating the next period')
@types.generator
def ts_cmd(sample_rate, interval) -> typing.Iterator:

    threading.Timer()


@cli.command('trace')
@types.processor
def trace_cmd(lines: typing.Iterator) -> typing.Iterator:
    """Writes input to stdout."""
    try:
        for line in lines:
            click.echo(line)
            yield line
    except Exception as e:
        click.echo('Error tracing input. %s' % e, err=True)


if __name__ == '__main__':
    cli()