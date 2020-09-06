"""Define API endpoints for tags."""
from typing import Awaitable, Callable, Dict


class TagAPI:
    """Define a tag "manager" object."""

    def __init__(self, async_request: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._async_request = async_request

    async def async_delete_tag(self, tag: str) -> None:
        """Delete a tag.

        :param tag: The tag to delete
        :type tag: ``str``
        """
        await self._async_request("get", "tags/delete", params={"tag": tag})

    async def async_get_tags(self) -> Dict[str, int]:
        """Get a mapping of all tags in this account and how many times each is used.

        :rtype: ``Dict[str, int]``
        """
        resp = await self._async_request("get", "tags/get")
        return {tag.attrib["tag"]: int(tag.attrib["count"]) for tag in resp}

    async def async_rename_tag(self, old: str, new: str) -> None:
        """Rename a tag.

        :param old: The tag to rename
        :type old: ``str``
        :param new: The new name
        :type new: ``str``
        """
        await self._async_request("get", "tags/rename", params={"old": old, "new": new})
