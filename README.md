# ![logo](assets/prune.png) pruun

![](https://github.com/alexkosj/pruun/workflows/Run%20tests/badge.svg?branch=master)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](/LICENSE)
![python version](https://img.shields.io/badge/python-3.6%2C3.7%2C3.8-blue?logo=python)

Pruun is a CL utility for easily creating [AWS lambda deployment packages within Python virtualenvs](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-venv). It was designed to work as a simple, out-of-the-box solution that can be integrated into any deployment pipeline.

> NOTE: Supported OSs are Linux and MAC. Windows support is not fully tested at the moment.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pruun

```
pip install pruun
```

## Usage

For the following usage examples, let's imagine this is simple directory structure:

```
.
├── requirements.txt
└── my_lambda_handler.py
```

```sh-session
$ pruun --help
Usage: pruun [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  package  Creates deployment package .zip file in current directory.
$ pruun package my_lambda_handler.py
Locating all installed packages...  [####################################]  100%          
Creating deployment package...
Finit!
```

## Commands

### pruun package [OPTIONS] handler_path

```
Usage: pruun package [OPTIONS] handler_path

  Creates deployment package .zip file in current directory.

  handler_path (str): Name of Lambda handler file/directory.  Trailing slash
  for a directory path is optional.

  package-file (str, optional): Desired filename of deployment .zip file.
  Defaults to "deployment_package.zip".

Options:
  --package-file PATH  Desired filename of deployment .zip file.
  --help               Show this message and exit.
```

## Contributing

Set up the development environment by running `make setup`.

Before contributing a pull request, please make sure tests pass by running `make test`.
