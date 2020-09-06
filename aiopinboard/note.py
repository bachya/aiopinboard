"""Define API endpoints for nodes."""
from dataclasses import dataclass
from datetime import datetime
from typing import Awaitable, Callable, List

from defusedxml import ElementTree
import maya


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

    :param tree: The XML element tree to parse
    :type tree: ``ElementTree``
    :rtype: ``Note``
    """
    return Note(
        tree.attrib["id"],
        tree[0].text,
        tree[1].text,
        maya.parse(tree[2].text).datetime(),
        maya.parse(tree[3].text).datetime(),
        int(tree[4].text),
    )


class NoteAPI:  # pylint: disable=too-few-public-methods
    """Define a note "manager" object."""

    def __init__(self, async_request: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._async_request = async_request

    async def async_get_notes(self) -> List[Note]:
        """Get all notes.

        :rtype: ``List[Note]``
        """
        resp = await self._async_request("get", "notes/list")
        return [async_create_note_from_xml(note) for note in resp]
