"""Define API endpoints for bookmarks."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, cast

import arrow

from aiopinboard.helpers.types import DictType, ListDictType, ResponseType

DEFAULT_RECENT_BOOKMARKS_COUNT: int = 15


@dataclass
class Bookmark:
    """Define a representation of a Pinboard bookmark."""

    hash: str
    href: str
    title: str
    description: str
    last_modified: datetime
    tags: list[str]
    unread: bool
    shared: bool

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> Bookmark:
        """Create a bookmark from an API response.

        Args:
            data: The API response data.

        Returns:
            A Bookmark object.
        """
        return Bookmark(
            data["hash"],
            data["href"],
            data["description"],
            data["extended"],
            arrow.get(data["time"]).datetime,
            data["tags"].split(),
            data["toread"] == "yes",
            data["shared"] != "no",
        )


class BookmarkAPI:
    """Define an API "manager" object."""

    def __init__(self, async_request: Callable[..., Awaitable[ResponseType]]):
        """Initialize.

        Args:
            async_request: The request method from the Client object.
        """
        self._async_request = async_request

    async def async_add_bookmark(  # pylint: disable=too-many-arguments
        self,
        url: str,
        title: str,
        *,
        description: str | None = None,
        tags: list[str] | None = None,
        created_datetime: datetime | None = None,
        replace: bool = True,
        shared: bool = False,
        toread: bool = False,
    ) -> None:
        """Add a new bookmark.

        Args:
            url: The URL of the bookmark.
            title: The title of the bookmark.
            description: The optional description of the bookmark.
            tags: An optional list of tags to assign to the bookmark.
            created_datetime: The optional creation datetime to use (defaults to now).
            replace: Whether this should replace a bookmark with the same URL.
            shared: Whether this bookmark should be shared.
            toread: Whether this bookmark should be unread.
        """
        params: dict[str, Any] = {"url": url, "description": title}

        if description:
            params["extended"] = description
        if tags:
            params["tags"] = " ".join(tags)
        if created_datetime:
            params["dt"] = created_datetime.isoformat()

        params["replace"] = "yes" if replace else "no"
        params["shared"] = "yes" if shared else "no"
        params["toread"] = "yes" if toread else "no"

        await self._async_request("get", "posts/add", params=params)

    async def async_delete_bookmark(self, url: str) -> None:
        """Delete a bookmark by URL.

        Args:
            url: The URL of the bookmark to delete.
        """
        await self._async_request("get", "posts/delete", params={"url": url})

    async def async_get_all_bookmarks(  # pylint: disable=too-many-arguments
        self,
        *,
        tags: list[str] | None = None,
        start: int = 0,
        results: int | None = None,
        from_dt: datetime | None = None,
        to_dt: datetime | None = None,
    ) -> list[Bookmark]:
        """Get recent bookmarks.

        Args:
            tags: An optional list of tags to filter results by.
            start: The optional starting index to return (defaults to the start).
            results: The optional number of results (defaults to all).
            from_dt: The optional datetime to start from.
            to_dt: The optional datetime to end at.

        Returns:
            A list of Bookmark objects.
        """
        params: dict[str, Any] = {"start": start}

        if tags:
            params["tags"] = " ".join([str(tag) for tag in tags])
        if results:
            params["results"] = results
        if from_dt:
            params["fromdt"] = from_dt.isoformat()
        if to_dt:
            params["todt"] = to_dt.isoformat()

        data = cast(
            ListDictType, await self._async_request("get", "posts/all", params=params)
        )
        return [Bookmark.from_api_response(bookmark) for bookmark in data]

    async def async_get_bookmark_by_url(self, url: str) -> Bookmark | None:
        """Get bookmark by a URL.

        Args:
            url: The URL of the bookmark to get

        Returns:
            A bookmark object (or None if no bookmark exists for the URL).
        """
        data = cast(
            DictType, await self._async_request("get", "posts/get", params={"url": url})
        )

        try:
            return Bookmark.from_api_response(data["posts"][0])
        except IndexError:
            return None

    async def async_get_bookmarks_by_date(
        self, bookmarked_on: date, *, tags: list[str] | None = None
    ) -> list[Bookmark]:
        """Get bookmarks that were created on a specific date.

        Args:
            bookmarked_on: The date to examine.
            tags: An optional list of tags to filter results by.

        Returns:
            A list of Bookmark objects.
        """
        params: dict[str, Any] = {"dt": str(bookmarked_on)}

        if tags:
            params["tags"] = " ".join([str(tag) for tag in tags])

        data = cast(
            DictType, await self._async_request("get", "posts/get", params=params)
        )
        return [Bookmark.from_api_response(bookmark) for bookmark in data["posts"]]

    async def async_get_dates(
        self, *, tags: list[str] | None = None
    ) -> dict[date, int]:
        """Get a dictionary of dates and the number of bookmarks created on that date.

        Args:
            tags: An optional list of tags to filter results by.

        Returns:
            A dictionary of dates and the number of bookmarks for that date.
        """
        params: dict[str, Any] = {}

        if tags:
            params["tags"] = " ".join([str(tag) for tag in tags])

        data = cast(DictType, await self._async_request("get", "posts/dates"))

        return {
            arrow.get(date).datetime.date(): count
            for date, count in data["dates"].items()
        }

    async def async_get_last_change_datetime(self) -> datetime:
        """Return the most recent time a bookmark was added, updated or deleted.

        Returns:
            A datetime object.
        """
        data = cast(DictType, await self._async_request("get", "posts/update"))
        parsed = arrow.get(data["update_time"])
        return parsed.datetime

    async def async_get_recent_bookmarks(
        self,
        *,
        count: int = DEFAULT_RECENT_BOOKMARKS_COUNT,
        tags: list[str] | None = None,
    ) -> list[Bookmark]:
        """Get recent bookmarks.

        Args:
            count: The number of bookmarks to return (max of 100).
            tags: An optional list of tags to filter results by.

        Returns:
            A list of Bookmark objects.
        """
        params: dict[str, Any] = {"count": count}

        if tags:
            params["tags"] = " ".join([str(tag) for tag in tags])

        data = cast(
            DictType, await self._async_request("get", "posts/recent", params=params)
        )
        return [Bookmark.from_api_response(bookmark) for bookmark in data["posts"]]

    async def async_get_suggested_tags(self, url: str) -> dict[str, list[str]]:
        """Return a dictionary of popular and recommended tags for a URL.

        Args:
            url: The URL of the bookmark to delete.

        Returns:
            A dictionary of tags.
        """
        data = cast(
            ListDictType,
            await self._async_request("get", "posts/suggest", params={"url": url}),
        )
        return {k: v for d in data for k, v in d.items()}
