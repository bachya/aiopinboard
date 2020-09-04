"""Define tests for errors."""
from aiohttp import ClientSession
import pytest

from aiopinboard import API
from aiopinboard.errors import RequestError

from tests.common import TEST_API_TOKEN, load_fixture


@pytest.mark.asyncio
async def test_data_error(aresponses):
    """Test that a Pinboard data error is handled properly."""
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/delete",
        "get",
        aresponses.Response(text=load_fixture("error_response.xml"), status=200),
    )

    async with ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)
        with pytest.raises(RequestError) as err:
            await api.async_delete_bookmark("http://test.url")
        assert str(err.value) == "item not found"


@pytest.mark.asyncio
async def test_http_error(aresponses):
    """Test that an HTTP error is handled properly."""
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/delete",
        "get",
        aresponses.Response(text=None, status=500),
    )

    async with ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)
        with pytest.raises(RequestError):
            await api.async_delete_bookmark("http://test.url")
