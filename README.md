# 📌 aiopinboard: A Python3 library for Elexa Guardian devices

[![CI](https://github.com/bachya/aiopinboard/workflows/CI/badge.svg)](https://github.com/bachya/aiopinboard/actions)
[![PyPi](https://img.shields.io/pypi/v/aiopinboard.svg)](https://pypi.python.org/pypi/aiopinboard)
[![Version](https://img.shields.io/pypi/pyversions/aiopinboard.svg)](https://pypi.python.org/pypi/aiopinboard)
[![License](https://img.shields.io/pypi/l/aiopinboard.svg)](https://github.com/bachya/aiopinboard/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/aiopinboard/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/aiopinboard)
[![Maintainability](https://api.codeclimate.com/v1/badges/a03c9e96f19a3dc37f98/maintainability)](https://codeclimate.com/github/bachya/aiopinboard/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

`aiopinboard` is a Python3, `asyncio`-focused library for interacting with
[Pinboard](https://pinboard.in) API.

- [Installation](#installation)
- [Python Versions](#python-versions)
- [API Token](#api-token)
- [Usage](#usage)
- [Contributing](#contributing)

# Installation

```python
pip install aiopinboard
```

# Python Versions

`aiopinboard` is currently supported on:

* Python 3.6
* Python 3.7
* Python 3.8 

# API Token

You can retrieve your Pinboard API token via
[your account's settings page](https://pinboard.in/settings/password).

# Usage

`aiopinboard` endeavors to replicate all of the endpoints
[the Pinboard API documentation](https://pinboard.in/api) with sane, usable responses.

All API usage starts with creating an `API` object that contains your Pinboard API token:

```python
import asyncio

from aiopinboard import Client


async def main() -> None:
    api = API("<PINBOARD_API_TOKEN>")
    # do things!


asyncio.run(main())
```

## Getting the Last Change Datetime

To get the UTC datetime of the last "change" (bookmark added, updated, or deleted):

```python
import asyncio

from aiopinboard import Client


async def main() -> None:
    api = API("<PINBOARD_API_TOKEN>")
    last_change_dt = await.async_get_last_change_datetime()
    # >>> datetime.datetime(2020, 9, 3, 13, 7, 19, tzinfo=<UTC>)


asyncio.run(main())
```

This method should be used to determine whether additional API calls should be made –
for example, if nothing has changed since the last time a request was made, the
implementing library can halt.

## Delete a Bookmark

To delete a bookmark by its URL:

```python
import asyncio

from aiopinboard import Client


async def main() -> None:
    api = API("<PINBOARD_API_TOKEN>")
    await api.async_delete_bookmark("https://my.com/bookmark")


asyncio.run(main())
```

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/aiopinboard/issues)
  or [initiate a discussion on one](https://github.com/bachya/aiopinboard/issues/new).
2. [Fork the repository](https://github.com/bachya/aiopinboard/fork).
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `script/test`
9. Update `README.md` with any new documentation.
10. Add yourself to `AUTHORS.md`.
11. Submit a pull request!
