"""Define API endpoints for tags."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import cast

from aiopinboard.helpers.types import ResponseType


class TagAPI:
    """Define a tag "manager" object."""

    def __init__(self, async_request: Callable[..., Awaitable[ResponseType]]) -> None:
        """Initialize.

        Args:
            async_request: The request method from the Client object.
        """
        self._async_request = async_request

    async def async_delete_tag(self, tag: str) -> None:
        """Delete a tag.

        Args:
            tag: The tag to delete.
        """
        await self._async_request("get", "tags/delete", params={"tag": tag})

    async def async_get_tags(self) -> dict[str, int]:
        """Get a mapping of all tags in this account and how many times each is used.

        Returns:
            A dictionary of tags and usage count.
        """
        return cast(dict[str, int], await self._async_request("get", "tags/get"))

    async def async_rename_tag(self, old: str, new: str) -> None:
        """Rename a tag.

        Args:
            old: The tag to rename.
            new: The new name.
        """
        await self._async_request("get", "tags/rename", params={"old": old, "new": new})
