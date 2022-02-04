# Shulker Box

[![python](https://img.shields.io/static/v1?label=python&message=3.10%2B&color=informational&logo=python&logoColor=white)](https://www.python.org/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![CircleCI](https://circleci.com/gh/microcraft-alpha/shulker-box/tree/main.svg?style=svg)](https://circleci.com/gh/microcraft-alpha/shulker-box/tree/main)

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Development](#development)

## 🧐 About <a name = "about"></a>

Simple `FastAPI` application that manages Minecraft items. This time I wanted to build the project around `MongoDB` database and `Beanie` ORM. For more information about the code structure please visit my another Minecraft-related `FastAPI` project, [Monster Spawner](https://github.com/microcraft-alpha/monster-spawner).

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

To get started you need to have `Docker` installed and optionally `Poetry`, if you want to have virtual environment locally. All the needed commands are available via `Makefile`.

### Installing

First, build the images.

```bash
make build
```

Then, you can just start the containers.

```bash
make up
```

After that, you should be able to see the output from the `FastAPI` server. It will be running on port `8003`, so you can access the documentation via `http://localhost:8003/api/docs`.

## 🎈 Usage <a name = "usage"></a>

There are also few useful commands to help manage the project.

If you have `Poetry` installed, you can run below command to have all the dependencies installed locally.

```bash
make install
```

In case you want to avoid installing anything locally, you can enter server container and run other commands from there.

```bash
make enter
```

## 🔧 Development <a name = "development"></a>

To make development smoother, this project supports `pre-commit` hooks for linting and code formatting along with `pytest` for testing. All the configs can be found in `.pre-commit-config.yaml` and `pyproject.toml` files.

To install the hooks, run the following command.

```bash
pre-commit install
```

Then you can use the following to run the hooks.

```bash
make lint
```

There is also a command for running tests.

```bash
make test
```

`pytest` is configured to clean the database after every test. Tests are also using different sessions to have a clean separation. You can check more fixtures in the `conftest.py` file, or the general configuration in the `pytest.ini` section.
