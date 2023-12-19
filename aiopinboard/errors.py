"""Define exception types for ``aiopinboard``."""
from __future__ import annotations

from aiopinboard.helpers.types import ResponseType


class PinboardError(Exception):
    """Define a base Pinboard exception."""

    pass


class RequestError(PinboardError):
    """Define a exception related to HTTP request errors."""

    pass


def raise_on_response_error(data: ResponseType) -> None:
    """Raise an error if the data indicates that something went wrong.

    Args:
        data: A response payload from the API.

    Raises:
        RequestError: Raised upon any error from the API.
    """
    if isinstance(data, list):
        return

    if (code := data.get("result_code")) is None:
        return

    if code == "done":
        return

    raise RequestError(code)
