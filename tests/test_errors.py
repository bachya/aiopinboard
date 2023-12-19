"""Define tests for errors."""
from typing import Any

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aiopinboard import API
from aiopinboard.errors import RequestError
from tests.common import TEST_API_TOKEN


@pytest.mark.asyncio
async def test_data_error(
    aresponses: ResponsesMockServer, error_response: dict[str, Any]
) -> None:
    """Test that a Pinboard data error is handled properly.

    Args:
        aresponses: An aresponses server.
        error_response: A Pinboard error response.
    """
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/delete",
        "get",
        response=aiohttp.web_response.json_response(error_response, status=200),
    )

    async with aiohttp.ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)
        with pytest.raises(RequestError) as err:
            await api.bookmark.async_delete_bookmark("http://test.url")
        assert str(err.value) == "item not found"


@pytest.mark.asyncio
async def test_http_error(aresponses: ResponsesMockServer) -> None:
    """Test that an HTTP error is handled properly.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/delete",
        "get",
        response=aresponses.Response(text=None, status=500),
    )

    async with aiohttp.ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)
        with pytest.raises(RequestError):
            await api.bookmark.async_delete_bookmark("http://test.url")
