"""Test the API."""
from datetime import datetime

from aiohttp import ClientSession
import pytest
import pytz

from aiopinboard import API
from aiopinboard.errors import RequestError
from aiopinboard.helpers.bookmark import Bookmark

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
async def test_delete_bookmark(aresponses):
    """Test deleting a bookmark."""
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/delete",
        "get",
        aresponses.Response(text=load_fixture("posts_delete_response.xml"), status=200),
    )

    async with ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)

        # A unsuccessful request will throw an exception, so if no exception is thrown,
        # we can count this as a successful test:
        await api.async_delete_bookmark("http://test.url")


@pytest.mark.asyncio
async def test_get_bookmarks_by_date(aresponses):
    """Test getting bookmarks by date."""
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/get",
        "get",
        aresponses.Response(text=load_fixture("posts_get_response.xml"), status=200),
    )

    async with ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)
        bookmarks = await api.async_get_bookmarks_by_date(
            pytz.utc.localize(datetime(2020, 9, 3, 13, 7, 19))
        )
        assert len(bookmarks) == 1
        assert bookmarks[0] == Bookmark(
            "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "https://mylink.com",
            "A really neat website!",
            "I saved this bookmark to Pinboard",
            pytz.utc.localize(datetime(2020, 9, 2, 3, 59, 55)),
            tags=["tag1", "tag2"],
            unread=True,
            shared=False,
        )


@pytest.mark.asyncio
async def test_get_last_change_datetime(aresponses):
    """Test getting the last time a bookmark was altered."""
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/update",
        "get",
        aresponses.Response(text=load_fixture("posts_update_response.xml"), status=200),
    )

    async with ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)
        most_recent_dt = await api.async_get_last_change_datetime()

        assert most_recent_dt == pytz.utc.localize(datetime(2020, 9, 3, 13, 7, 19))


@pytest.mark.asyncio
async def test_get_last_change_datetime_no_session(aresponses):
    """Test getting the last time a bookmark was altered.

    Note that this test also tests a created-on-the-fly ClientSession.
    """
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/update",
        "get",
        aresponses.Response(text=load_fixture("posts_update_response.xml"), status=200),
    )

    api = API(TEST_API_TOKEN)
    most_recent_dt = await api.async_get_last_change_datetime()

    assert most_recent_dt == pytz.utc.localize(datetime(2020, 9, 3, 13, 7, 19))


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
