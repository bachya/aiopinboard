"""Define API endpoints for tags."""
from __future__ import annotations

from collections.abc import Awaitable, Callable

from defusedxml import ElementTree


class TagAPI:
    """Define a tag "manager" object."""

    def __init__(self, async_request: Callable[..., Awaitable[ElementTree]]) -> None:
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
        resp = await self._async_request("get", "tags/get")
        return {tag.attrib["tag"]: int(tag.attrib["count"]) for tag in resp}

    async def async_rename_tag(self, old: str, new: str) -> None:
        """Rename a tag.

        Args:
            old: The tag to rename.
            new: The new name.
        """
        await self._async_request("get", "tags/rename", params={"old": old, "new": new})
