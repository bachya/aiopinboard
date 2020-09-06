"""Define API endpoints for bookmarks."""
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Awaitable, Callable, Dict, List, Optional

from defusedxml import ElementTree
import maya

DEFAULT_RECENT_BOOKMARKS_COUNT: int = 15


@dataclass
class Bookmark:  # pylint: disable=too-many-instance-attributes
    """Define a representation of a Pinboard bookmark."""

    hash: str
    href: str
    title: str
    description: str
    last_modified: datetime
    tags: List[str]
    unread: bool
    shared: bool


def async_create_bookmark_from_xml(tree: ElementTree) -> Bookmark:
    """Create a bookmark from an XML response.

    :param tree: The XML element tree to parse
    :type tree: ``ElementTree``
    :rtype: ``Bookmark``
    """
    return Bookmark(
        tree.attrib["hash"],
        tree.attrib["href"],
        tree.attrib["description"],
        tree.attrib["extended"],
        maya.parse(tree.attrib["time"]).datetime(),
        tree.attrib["tag"].split(),
        tree.attrib.get("toread") == "yes",
        tree.attrib.get("shared") == "yes",
    )


class BookmarkAPI:
    """Define an API "manager" object."""

    def __init__(self, async_request: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._async_request = async_request

    async def async_add_bookmark(
        self,
        url: str,
        title: str,
        *,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        created_datetime: Optional[datetime] = None,
        replace: bool = True,
        shared: bool = False,
        toread: bool = False,
    ) -> None:
        """Add a new bookmark.

        :param url: The URL of the bookmark
        :type url: ``str``
        :param title: The title of the bookmark
        :type title: ``str``
        :param description: The optional description of the bookmark
        :type description: ``Optional[str]``
        :param tags: An optional list of tags to assign to the bookmark
        :type tags: ``Optional[List[str]]``
        :param created_datetime: The optional creation datetime to use (defaults to now)
        :type created_datetime: ``Optional[datetime]``
        :param replace: Whether this should replace a bookmark with the same URL
        :type replace: ``bool``
        :param shared: Whether this bookmark should be shared
        :type shared: ``bool``
        :param toread: Whether this bookmark should be unread
        :type toread: ``bool``
        :rtype: ``Bookmark``
        """
        params: Dict[str, Any] = {"url": url, "description": title}

        if description:
            params["description"] = description
        if tags:
            params["tags"] = tags
        if created_datetime:
            params["dt"] = created_datetime.isoformat()

        params["replace"] = "yes" if replace else "no"
        params["shared"] = "yes" if shared else "no"
        params["toread"] = "yes" if toread else "no"

        await self._async_request("get", "posts/add", params=params)

    async def async_delete_bookmark(self, url: str) -> None:
        """Delete a bookmark by URL.

        :param url: The URL of the bookmark to delete
        :type url: ``str``
        """
        await self._async_request("get", "posts/delete", params={"url": url})

    async def async_get_all_bookmarks(
        self,
        *,
        tags: Optional[List[str]] = None,
        start: int = 0,
        results: Optional[int] = None,
        from_dt: Optional[datetime] = None,
        to_dt: Optional[datetime] = None,
    ) -> List[Bookmark]:
        """Get recent bookmarks.

        :param tags: An optional list of tags to filter results by
        :type tags: ``Optional[List[str]]``
        :param start: The optional starting index to return (defaults to the start)
        :type start: ``int``
        :param results: The optional number of results (defaults to all)
        :type results: ``int``
        :param from_dt: The optional datetime to start from
        :type from_dt: ``Optional[datetime]``
        :param to_dt: The optional datetime to end at
        :type to_dt: ``Optional[datetime]``
        :rtype: ``List[Bookmark]``
        """
        params: Dict[str, Any] = {"start": start}

        if tags:
            params["tags"] = " ".join([str(tag) for tag in tags])
        if results:
            params["results"] = results
        if from_dt:
            params["fromdt"] = from_dt.isoformat()
        if to_dt:
            params["fromdt"] = to_dt.isoformat()

        resp = await self._async_request("get", "posts/all", params=params)
        return [async_create_bookmark_from_xml(bookmark) for bookmark in resp]

    async def async_get_bookmark_by_url(self, url: str) -> Optional[Bookmark]:
        """Get bookmark by a URL. Returns None if no bookmark exists for URL.

        :param url: The URL of the bookmark to get
        :type url: ``Optional[Bookmark]``
        :rtype: ``Optional[Bookmark]``
        """
        resp = await self._async_request("get", "posts/get", params={"url": url})

        try:
            return async_create_bookmark_from_xml(resp[0])
        except IndexError:
            return None

    async def async_get_bookmarks_by_date(
        self, bookmarked_on: date, *, tags: Optional[List[str]] = None
    ) -> List[Bookmark]:
        """Get bookmarks that were created on a specific date.

        :param bookmarked_on: The date to examine
        :type bookmarked_on: ``date``
        :param tags: An optional list of tags to filter results by
        :type tags: ``Optional[List[str]]``
        :rtype: ``List[Bookmark]``
        """
        params: Dict[str, Any] = {"dt": str(bookmarked_on)}

        if tags:
            params["tags"] = " ".join([str(tag) for tag in tags])

        resp = await self._async_request("get", "posts/get", params=params)
        return [async_create_bookmark_from_xml(bookmark) for bookmark in resp]

    async def async_get_dates(
        self, *, tags: Optional[List[str]] = None
    ) -> Dict[date, int]:
        """Get a dictionary of dates and the number of bookmarks created on that date.

        :param tags: An optional list of tags to filter results by
        :type tags: ``Optional[List[str]]``
        :rtype: ``Dict[date, int]``
        """
        params: Dict[str, Any] = {}

        if tags:
            params["tags"] = " ".join([str(tag) for tag in tags])

        resp = await self._async_request("get", "posts/dates")

        return {
            maya.parse(row.attrib["date"]).datetime().date(): int(row.attrib["count"])
            for row in resp
        }

    async def async_get_last_change_datetime(self) -> datetime:
        """Return the most recent time a bookmark was added, updated or deleted.

        :rtype: ``datetime``
        """
        resp = await self._async_request("get", "posts/update")
        maya_dt = maya.parse(resp.attrib["time"])
        return maya_dt.datetime()

    async def async_get_recent_bookmarks(
        self,
        *,
        count: int = DEFAULT_RECENT_BOOKMARKS_COUNT,
        tags: Optional[List[str]] = None,
    ) -> List[Bookmark]:
        """Get recent bookmarks.

        :param count: The number of bookmarks to return (max of 100)
        :type count: ``int``
        :param tags: An optional list of tags to filter results by
        :type tags: ``Optional[List[str]]``
        :rtype: ``List[Bookmark]``
        """
        params: Dict[str, Any] = {"count": count}

        if tags:
            params["tags"] = " ".join([str(tag) for tag in tags])

        resp = await self._async_request("get", "posts/recent", params=params)
        return [async_create_bookmark_from_xml(bookmark) for bookmark in resp]

    async def async_get_suggested_tags(self, url: str) -> Dict[str, List[str]]:
        """Return a dictionary of popular and recommended tags for a URL.

        :param url: The URL of the bookmark to delete
        :type url: ``str``
        """
        data: Dict[str, List[str]] = {"popular": [], "recommended": []}

        resp = await self._async_request("get", "posts/suggest", params={"url": url})
        for tag in resp:
            if tag.text not in data[tag.tag]:
                data[tag.tag].append(tag.text)

        return data
