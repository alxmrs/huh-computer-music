# huh-computer-music

This is a tiny computer music library writing in Python, powered by NumPy. 
Here, we use principles behind analog synthesizers to make computer music. 

For an idea of what this means, check out the [demo notebook](/demos/Pycon2018-talk.ipynb).

## Installation

1. Clone this repository
2. `pip install -e .`

### Developer setup

`pip install -e .[dev]`

## Usage

### CLI

`bish` is an experimental script to pipeline commands for sound generation.

`bish --help` will print the full list of commands. 

Each command comes with aliases. They can either be called by their partial name (`multiply` --> `mul`) or 
by their initials (`time-series` --> `ts`).

`bish <cmd> --help` will print the unabridged docs for the command.

#### Examples

`bish period trace ts osc scale-map vco mul -v 0.05 trace speaker`

TODO(#13)

### Library

The library is under revision. Usage can be demonstrated via [this demo notebook](demos/huh_computer_music.ipynb).

TODO(#14)

