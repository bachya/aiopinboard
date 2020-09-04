"""Define an API object to interact with the Pinboard API."""
from datetime import date, datetime
import logging
from typing import List, Optional

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError
from defusedxml import ElementTree
import maya

from aiopinboard.errors import RequestError, raise_on_response_error
from aiopinboard.helpers.bookmark import Bookmark

_LOGGER = logging.getLogger(__name__)

API_URL_BASE = "https://api.pinboard.in/v1"

DEFAULT_TIMEOUT: int = 10


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


class API:
    """Define an API object.

    :param api_token: A Pinboard API token
    :type api_token: ``str``
    :param session: An optional ``aiohttp`` ``ClientSession``
    :type api_token: ``Optional[ClientSession]``
    """

    def __init__(
        self, api_token: str, *, session: Optional[ClientSession] = None
    ) -> None:
        """Initialize."""
        self._api_token = api_token
        self._session: ClientSession = session

    async def _async_request(self, method: str, endpoint: str, **kwargs) -> ElementTree:
        """Make a request to the API and return the XML response."""
        kwargs.setdefault("params", {})
        kwargs["params"]["auth_token"] = self._api_token

        use_running_session = self._session and not self._session.closed

        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        try:
            async with session.request(
                method, f"{API_URL_BASE}/{endpoint}", **kwargs
            ) as resp:
                resp.raise_for_status()
                body = await resp.text()

                _LOGGER.debug("Response text for %s: %s", endpoint, body)

                response_root = ElementTree.fromstring(body.encode("utf-8"))
                raise_on_response_error(response_root)

                return response_root
        except ClientError as err:
            raise RequestError(err)
        finally:
            if not use_running_session:
                await session.close()

    async def async_delete_bookmark(self, url: str) -> None:
        """Delete a bookmark by URL.

        :param url: The URL of the bookmark to delete
        :type url: ``str``
        """
        await self._async_request("get", "posts/delete", params={"url": url})

    async def async_get_bookmark_by_url(self, url: str) -> Optional[Bookmark]:
        """Get bookmark by a URL. Returns None if no bookmark exists for URL.

        :param url: The URL of the bookmark to get
        :type url: ``Optional[Bookmark]``
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
        """
        params = {"dt": str(bookmarked_on)}
        if tags:
            params["tags"] = " ".join([str(tag) for tag in tags])

        resp = await self._async_request("get", "posts/get", params=params)
        return [async_create_bookmark_from_xml(bookmark) for bookmark in resp]

    async def async_get_last_change_datetime(self) -> datetime:
        """Return the most recent time a bookmark was added, updated or deleted."""
        resp = await self._async_request("get", "posts/update")
        maya_dt = maya.parse(resp.attrib["time"])
        return maya_dt.datetime()
