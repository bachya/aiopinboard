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


class API:
    """Define an API object."""

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
                response_root = ElementTree.fromstring(body.encode("utf-8"))
                raise_on_response_error(response_root)
                return response_root
        except ClientError as err:
            raise RequestError(err)
        finally:
            if not use_running_session:
                await session.close()

    async def async_delete_bookmark(self, url: str) -> None:
        """Delete a bookmark by URL."""
        await self._async_request("get", "posts/delete", params={"url": url})

    async def async_get_bookmarks_by_date(self, the_date: date) -> List[Bookmark]:
        """Get bookmarks by date bookmarked."""
        resp = await self._async_request(
            "get", "posts/get", params={"dt": str(the_date)}
        )

        return [
            Bookmark(
                bookmark.attrib["hash"],
                bookmark.attrib["href"],
                bookmark.attrib["description"],
                bookmark.attrib["extended"],
                maya.parse(bookmark.attrib["time"]).datetime(),
                bookmark.attrib["tag"].split(),
                bookmark.attrib.get("toread") == "yes",
                bookmark.attrib.get("shared") == "yes",
            )
            for bookmark in resp
        ]

    async def async_get_last_change_datetime(self) -> datetime:
        """Return the most recent time a bookmark was added, updated or deleted."""
        resp = await self._async_request("get", "posts/update")
        maya_dt = maya.parse(resp.attrib["time"])
        return maya_dt.datetime()
