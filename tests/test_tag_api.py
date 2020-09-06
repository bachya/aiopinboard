"""Test tag API endpoints."""
from aiohttp import ClientSession
import pytest

from aiopinboard import API

from tests.common import TEST_API_TOKEN, load_fixture


@pytest.mark.asyncio
async def test_delete_tag(aresponses):
    """Test deleting a tag."""
    aresponses.add(
        "api.pinboard.in",
        "/v1/tags/delete",
        "get",
        aresponses.Response(text=load_fixture("tags_delete_response.xml"), status=200),
    )

    async with ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)

        # A unsuccessful request will throw an exception, so if no exception is thrown,
        # we can count this as a successful test:
        await api.tag.async_delete_tag("tag1")


@pytest.mark.asyncio
async def test_get_tags(aresponses):
    """Test getting tags."""
    aresponses.add(
        "api.pinboard.in",
        "/v1/tags/get",
        "get",
        aresponses.Response(text=load_fixture("tags_get_response.xml"), status=200),
    )

    async with ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)

        tags = await api.tag.async_get_tags()
        assert tags == {"tag1": 3, "tag2": 1, "tag3": 2}


@pytest.mark.asyncio
async def test_rename_tag(aresponses):
    """Test renaming a tag."""
    aresponses.add(
        "api.pinboard.in",
        "/v1/tags/rename",
        "get",
        aresponses.Response(text=load_fixture("tags_rename_response.xml"), status=200),
    )

    async with ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)

        # A unsuccessful request will throw an exception, so if no exception is thrown,
        # we can count this as a successful test:
        await api.tag.async_rename_tag("tag1", "new-tag1")
