"""Define API endpoints for nodes."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import datetime

import arrow
from defusedxml import ElementTree


@dataclass
class Note:  # pylint: disable=too-many-instance-attributes
    """Define a representation of a Pinboard note."""

    note_id: str
    title: str
    hash: str
    created_at: datetime
    updated_at: datetime
    length: int


def async_create_note_from_xml(tree: ElementTree) -> Note:
    """Create a note from an XML response.

    Args:
        tree: A parsed XML tree.

    Returns:
        A Note object.
    """
    return Note(
        tree.attrib["id"],
        tree[0].text,
        tree[1].text,
        arrow.get(tree[2].text).datetime,
        arrow.get(tree[3].text).datetime,
        int(tree[4].text),
    )


class NoteAPI:  # pylint: disable=too-few-public-methods
    """Define a note "manager" object."""

    def __init__(self, async_request: Callable[..., Awaitable[ElementTree]]) -> None:
        """Initialize.

        Args:
            async_request: The request method from the Client object.
        """
        self._async_request = async_request

    async def async_get_notes(self) -> list[Note]:
        """Get all notes.

        Returns:
            A list of Note objects.
        """
        resp = await self._async_request("get", "notes/list")
        return [async_create_note_from_xml(note) for note in resp]
