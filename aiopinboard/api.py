"""Define an API object to interact with the Pinboard API."""
from __future__ import annotations

import logging
from typing import Any

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

    def __init__(self, api_token: str, *, session: ClientSession | None = None) -> None:
        """Initialize.

        Args:
            api_token: A Pinboard API token.
            session: An optional aiohttp ClientSession.
        """
        self._api_token = api_token
        self._session = session

        self.bookmark = BookmarkAPI(self._async_request)
        self.note = NoteAPI(self._async_request)
        self.tag = TagAPI(self._async_request)

    async def _async_request(
        self, method: str, endpoint: str, **kwargs: dict[str, Any]
    ) -> ElementTree:
        """Make a request to the API and return the XML response.

        Args:
            method: An HTTP method.
            endpoint: A relative API endpoint.
            **kwargs: Additional kwargs to send with the request.

        Returns:
            An API response payload.

        Raises:
            RequestError: Raised upon an underlying HTTP error.
        """
        kwargs.setdefault("params", {})
        kwargs["params"]["auth_token"] = self._api_token

        if use_running_session := self._session and not self._session.closed:
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
            raise RequestError(err) from None
        finally:
            if not use_running_session:
                await session.close()
