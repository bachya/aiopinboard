"""Define exception types for ``aiopinboard``."""
from defusedxml import ElementTree


class PinboardError(Exception):
    """Define a base Pinboard exception."""

    pass


class RequestError(PinboardError):
    """Define a exception related to HTTP request errors."""

    pass


def raise_on_response_error(response_root: ElementTree) -> None:
    """Raise an error if the data indicates that something went wrong."""
    if "code" not in response_root.attrib:
        return

    if response_root.attrib["code"] == "done":
        return

    raise RequestError(response_root.attrib["code"])
