# PyFuck

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about">Pyfuck</a>

PyFuck is a CLI tool to run and debug Brainfuck code. Written in python

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

A good OS (Linux) and python. Clone the repo and cd into it 

```bash
git clone https://github.com/Muxutruk2/Pyfuck.git && cd Pyfuck
```

### Installing

Install the required libraries

```bash
pip install requirements.txt
```

Now test the app doing:
```bash
python pyfuck.py examples/helloworld1.bf
```

## Usage <a name = "usage"></a>

To run a bf file use the syntax above ↑

To debug a file use the --debug or -d flags. You can set the tick interval (in seconds) with -i

```bash
python pyfuck.py examples/helloworld1.bf -d -i 0.001
```

To DEBUG-DEBUG use -dd. This is for a step-by-step proccess

```bash
python pyfuck.py examples/helloworld1.bf -d -i 0.001
```

And no, there is no -ddd flag.
