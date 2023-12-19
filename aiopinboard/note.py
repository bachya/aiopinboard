"""Define API endpoints for nodes."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any, cast

import arrow

from aiopinboard.helpers.types import DictType, ResponseType


@dataclass
class Note:  # pylint: disable=too-many-instance-attributes
    """Define a representation of a Pinboard note."""

    note_id: str
    title: str
    hash: str
    created_at: datetime
    updated_at: datetime
    length: int

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> Note:
        """Create a note from an API response.

        Args:
            data: The API response data.

        Returns:
            A Note object.
        """
        return cls(
            data["id"],
            data["title"],
            data["hash"],
            arrow.get(data["created_at"]).datetime,
            arrow.get(data["updated_at"]).datetime,
            data["length"],
        )


class NoteAPI:  # pylint: disable=too-few-public-methods
    """Define a note "manager" object."""

    def __init__(self, async_request: Callable[..., Awaitable[ResponseType]]) -> None:
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
        data = cast(DictType, await self._async_request("get", "notes/list"))
        return [Note.from_api_response(note) for note in data["notes"]]
