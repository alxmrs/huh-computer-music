# huh-computer-music

This is a tiny computer music library writing in Python, powered by NumPy. 
Here, we use principles behind analog synthesizers to make computer music. 

For an idea of what this means, check out the [demo notebook](/demos/huh_computer_music.ipynb).

## Installation

`pip install git+https://github.com/alxmrs/huh-computer-music.git`

## Usage

This package is best used as the library `hcm` in a juptyer notebook. Usage
can be demonstrated via [this demo notebook](demos/huh_computer_music.ipynb).

TODO(#14)

### CLI

`bish` is an experimental script to pipeline commands for sound generation. This script is included in installation.

`bish --help` will print the full list of commands.

Each command comes with aliases. They can either be called by their partial name (`multiply` --> `mul`) or
by their initials (`time-series` --> `ts`).

`bish <cmd> --help` will print the unabridged docs for the command.

#### Examples

`bish period trace ts osc scale-map vco mul -c 0.05 trace speaker`

TODO(#13)
