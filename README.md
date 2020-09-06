# 📌 aiopinboard: A Python 3 Library for Pinboard

[![CI](https://github.com/bachya/aiopinboard/workflows/CI/badge.svg)](https://github.com/bachya/aiopinboard/actions)
[![PyPi](https://img.shields.io/pypi/v/aiopinboard.svg)](https://pypi.python.org/pypi/aiopinboard)
[![Version](https://img.shields.io/pypi/pyversions/aiopinboard.svg)](https://pypi.python.org/pypi/aiopinboard)
[![License](https://img.shields.io/pypi/l/aiopinboard.svg)](https://github.com/bachya/aiopinboard/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/aiopinboard/branch/dev/graph/badge.svg)](https://codecov.io/gh/bachya/aiopinboard)
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

## The `Bookmark` Object

API endpoints that retrieve one or more bookmarks will return `Bookmark` objects, which
carry all of the expected properties of a bookmark:

* `hash`: the unique identifier of the bookmark
* `href`: the bookmark's URL
* `title`: the bookmark's title
* `description`: the bookmark's description
* `last_modified`: the UTC date the bookmark was last modified
* `tags`: a list of tags applied to the bookmark
* `unread`: whether the bookmark is unread
* `shared`: whether the bookmark is shared

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

## Getting a Bookmark

To get a bookmark by its URL:

```python
import asyncio

from aiopinboard import Client


async def main() -> None:
    api = API("<PINBOARD_API_TOKEN>")
    await api.async_get_bookmark_by_url("https://my.com/bookmark")
    # >>> <Bookmark href="https://my.com/bookmark">


asyncio.run(main())
```

To get all bookmarks created on a certain date:


```python
import asyncio
from datetime import date

from aiopinboard import Client


async def main() -> None:
    api = API("<PINBOARD_API_TOKEN>")
    await api.async_get_bookmarks_by_date(date.today())
    # >>> [<Bookmark ...>, <Bookmark ...>]

    # Optionally filter the results with a list of tags – note that only bookmarks that
    # have all tags will be returned:
    await api.async_get_bookmarks_by_date(
        datetime(2020, 9, 2, 3, 59, 55), tags=["tag1", "tag2"]
    )
    # >>> [<Bookmark ...>, <Bookmark ...>]
)


asyncio.run(main())
```

## Adding a Bookmark

To add a bookmark:

```python
import asyncio

from aiopinboard import Client


async def main() -> None:
    api = API("<PINBOARD_API_TOKEN>")
    await api.async_add_bookmark("https://my.com/bookmark", "My New Bookmark")


asyncio.run(main())
```

You can specify several optional parameters while editing a bookmark:

* `description`: the optional description of the bookmark
* `tags`: an optional list of tags to assign to the bookmark
* `created_datetime`: the optional creation datetime to use (defaults to now)
* `replace`: whether this should replace a bookmark with the same URL
* `shared`: whether this bookmark should be shared
* `toread`: whether this bookmark should be unread

## Deleting a Bookmark

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
