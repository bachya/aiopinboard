"""Define an API object to interact with the Pinboard API."""
import logging
from typing import Optional

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError
from defusedxml import ElementTree

from aiopinboard.bookmark import BookmarkAPI
from aiopinboard.errors import RequestError, raise_on_response_error
from aiopinboard.note import NoteAPI
from aiopinboard.tag import TagAPI

_LOGGER = logging.getLogger(__name__)

API_URL_BASE: str = "https://api.pinboard.in/v1"

DEFAULT_TIMEOUT: int = 10


class API:  # pylint: disable=too-few-public-methods
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

        self.bookmark = BookmarkAPI(self._async_request)
        self.note = NoteAPI(self._async_request)
        self.tag = TagAPI(self._async_request)

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
