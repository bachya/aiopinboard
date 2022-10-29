"""Test the API."""
from datetime import datetime, timedelta

import maya
import pytest
import pytz
from aiohttp import ClientSession
from aresponses import ResponsesMockServer

from aiopinboard import API
from aiopinboard.bookmark import Bookmark
from tests.common import TEST_API_TOKEN, load_fixture


@pytest.mark.asyncio
async def test_add_bookmark(aresponses: ResponsesMockServer) -> None:
    """Test deleting a bookmark.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/add",
        "get",
        aresponses.Response(text=load_fixture("posts_add_response.xml"), status=200),
    )

    async with ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)

        # A unsuccessful request will throw an exception, so if no exception is thrown,
        # we can count this as a successful test:
        await api.bookmark.async_add_bookmark(
            "http://test.url",
            "My Test Bookmark",
            description="I like this bookmark",
            tags=["tag1", "tag2"],
            created_datetime=datetime.now(),
            replace=True,
            shared=True,
            toread=True,
        )


@pytest.mark.asyncio
async def test_delete_bookmark(aresponses: ResponsesMockServer) -> None:
    """Test deleting a bookmark.

    Args:
        aresponses: An aresponses server.
    """
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
        await api.bookmark.async_delete_bookmark("http://test.url")


@pytest.mark.asyncio
async def test_get_all_bookmarks(aresponses: ResponsesMockServer) -> None:
    """Test getting recent bookmarks.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/all",
        "get",
        aresponses.Response(text=load_fixture("posts_all_response.xml"), status=200),
    )

    async with ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)

        bookmarks = await api.bookmark.async_get_all_bookmarks(
            tags=["tag1"],
            start=2,
            results=1,
            from_dt=datetime.now(),
            to_dt=datetime.now() + timedelta(days=2),
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
async def test_get_bookmark_by_url(aresponses: ResponsesMockServer) -> None:
    """Test getting bookmarks by date.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/get",
        "get",
        aresponses.Response(text=load_fixture("posts_get_response.xml"), status=200),
    )
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/get",
        "get",
        aresponses.Response(
            text=load_fixture("posts_get_empty_response.xml"), status=200
        ),
    )

    async with ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)

        bookmark = await api.bookmark.async_get_bookmark_by_url("https://mylink.com")
        assert bookmark == Bookmark(
            "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "https://mylink.com",
            "A really neat website!",
            "I saved this bookmark to Pinboard",
            pytz.utc.localize(datetime(2020, 9, 2, 3, 59, 55)),
            tags=["tag1", "tag2"],
            unread=True,
            shared=False,
        )

        bookmark = await api.bookmark.async_get_bookmark_by_url(
            "https://doesntexist.com"
        )
        assert not bookmark


@pytest.mark.asyncio
async def test_get_bookmarks_by_date(aresponses: ResponsesMockServer) -> None:
    """Test getting bookmarks by date.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/get",
        "get",
        aresponses.Response(text=load_fixture("posts_get_response.xml"), status=200),
    )
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/get",
        "get",
        aresponses.Response(
            text=load_fixture("posts_get_empty_response.xml"), status=200
        ),
    )

    async with ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)

        bookmarks = await api.bookmark.async_get_bookmarks_by_date(
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

        bookmarks = await api.bookmark.async_get_bookmarks_by_date(
            pytz.utc.localize(datetime(2020, 9, 3, 13, 7, 19)), tags=["non-tag1"]
        )
        assert not bookmarks


@pytest.mark.asyncio
async def test_get_dates(aresponses: ResponsesMockServer) -> None:
    """Test getting bookmarks by date.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/dates",
        "get",
        aresponses.Response(text=load_fixture("posts_dates_response.xml"), status=200),
    )

    async with ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)

        dates = await api.bookmark.async_get_dates(tags=["tag1", "tag2"])
        assert dates == {
            maya.parse("2020-09-05").datetime().date(): 1,
            maya.parse("2020-09-04").datetime().date(): 1,
            maya.parse("2020-09-03").datetime().date(): 3,
        }


@pytest.mark.asyncio
async def test_get_last_change_datetime(aresponses: ResponsesMockServer) -> None:
    """Test getting the last time a bookmark was altered.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/update",
        "get",
        aresponses.Response(text=load_fixture("posts_update_response.xml"), status=200),
    )

    async with ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)
        most_recent_dt = await api.bookmark.async_get_last_change_datetime()

        assert most_recent_dt == pytz.utc.localize(datetime(2020, 9, 3, 13, 7, 19))


@pytest.mark.asyncio
async def test_get_last_change_datetime_no_session(
    aresponses: ResponsesMockServer,
) -> None:
    """Test getting the last time a bookmark was altered.

    Note that this test also tests a created-on-the-fly ClientSession.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/update",
        "get",
        aresponses.Response(text=load_fixture("posts_update_response.xml"), status=200),
    )

    api = API(TEST_API_TOKEN)
    most_recent_dt = await api.bookmark.async_get_last_change_datetime()

    assert most_recent_dt == pytz.utc.localize(datetime(2020, 9, 3, 13, 7, 19))


@pytest.mark.asyncio
async def test_get_recent_bookmarks(aresponses: ResponsesMockServer) -> None:
    """Test getting recent bookmarks.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/recent",
        "get",
        aresponses.Response(text=load_fixture("posts_recent_response.xml"), status=200),
    )

    async with ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)

        bookmarks = await api.bookmark.async_get_recent_bookmarks(
            count=1, tags=["tag1"]
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
async def test_get_suggested_tags(aresponses: ResponsesMockServer) -> None:
    """Test getting recent bookmarks.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "api.pinboard.in",
        "/v1/posts/suggest",
        "get",
        aresponses.Response(
            text=load_fixture("posts_suggest_response.xml"), status=200
        ),
    )

    async with ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)

        tags = await api.bookmark.async_get_suggested_tags("https://mylink.com")
        assert tags == {
            "popular": ["security"],
            "recommended": ["ssh", "linux"],
        }
