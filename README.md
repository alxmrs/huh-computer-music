# huh-computer-music

This is a tiny computer music library writing in Python, powered by NumPy. 
Here, we use principles behind analog synthesizers to make computer music. 

For an idea of what this means, check out the [demo notebook](/demos/Pycon2018-talk.ipynb).

## Installation

In a little while, this module will be pip-installable. For the time being, please clone or download this repository and
then install as follows: 

1. Create a virtual python environment using your favorite method. Or, simply call `make env`. 
2. Install the project requirements:
 - `make reqs`
 - or `pip3 install -r requirements.txt`

To view all workflow commands, simply run `make`.

## Usage

### CLI

`bish` is an experimental script to pipeline commands for sound generation.

`bish --help` will print the full list of commands. 

Each command comes with aliases: They can either be called by their partial name (`multiply` --> `mul`) or 
by their initials (`time-series` --> `ts`).

`bish <cmd> --help` will print the unabridged docs for the command.

#### Examples

`bish period trace ts osc scale-map vco mul -v 0.05 trace speaker`

TODO(#13)

### Library

The library is under revision. Usage can be demonstrated via [this demo notebook](demos/huh_computer_music.ipynb).

TODO(#14)

