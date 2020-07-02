# pruun

[![license](https://img.shields.io/badge/license-MIT-green.svg)](/LICENSE)
![python version](https://img.shields.io/badge/python-3.6%2C3.7%2C3.8-blue?logo=python)

Pruun is a CL utility for easily managing [AWS lambda deployment packages within virtualenvs](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-venv).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pruun

```bash
pip install pruun
```

## Usage

Imagine this is our directory structure:

```
.
├── requirements.txt
└── lambda_handler.py
```

### `pruun [OPTIONS] PATH/TO/LAMBDA/HANDLER/FILE`

Parses installed packages and creates a minimal .zip file
