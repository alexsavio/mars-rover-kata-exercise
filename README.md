# Mars Rover Kata

This my deliverable for the Mars Rover Kata from
Equal Experts (version 1.2, last updated on 2020-10-26).

## Issue description

You are part of the team that explores Mars by sending remotely controlled vehicles to the surface of
the planet.

Write an idiomatic piece of software that translates the commands sent from earth to
actions executed by the rover yielding a final state..

When the rover touches down on Mars, it is initialised with its current coordinates and the direction
it is facing. These could be any coordinates, supplied as arguments ​ (x, y, direction)​ e.g. ​ (4,
2, EAST)​ .

## Requirements

The setup for this project described here requires `make` and a
Python 3.9 installation.

It uses `poetry` for dependency management and installation.

### Installation

I recommend you to activate a Python environment and then run:

```bash
make install
```

or, the most important parts from the previous step you can get with:

```bash
pip install poetry
poetry install --no-dev
```

### Development

To work on this project you will need to install all development dependencies.
To do that you can run:

```bash
make install-dev
```

or,

```bash
pip install poetry
poetry install
```

#### Code quality

We use `tox` to run a set of code quality checks: `isort`, `mypy`, `lint`, and
`test`.

To run all of them, execute:

```bash
tox
```

Alternatively, you can run them separately, with:

```bash
tox -e test
```

where `test` can be replaced by the names mentioned above.

#### Testin

The tests alone can be executed with `pytest`. To run them you can also run
this after installing the dependencies:

```bash
pytest src
```
