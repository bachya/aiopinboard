"""Test tag API endpoints."""

from __future__ import annotations

from typing import Any

import aiohttp
from aresponses import ResponsesMockServer
import pytest

from aiopinboard import API
from tests.common import TEST_API_TOKEN


@pytest.mark.asyncio
async def test_delete_tag(
    aresponses: ResponsesMockServer, tags_delete_response: dict[str, Any]
) -> None:
    """Test deleting a tag.

    Args:
    ----
        aresponses: An aresponses server.
        tags_delete_response: A fixture for a tags/delete response payload.

    """
    aresponses.add(
        "api.pinboard.in",
        "/v1/tags/delete",
        "get",
        response=aiohttp.web_response.json_response(
            tags_delete_response, content_type="text/json", status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)

        # A unsuccessful request will throw an exception, so if no exception is thrown,
        # we can count this as a successful test:
        await api.tag.async_delete_tag("tag1")


@pytest.mark.asyncio
async def test_get_tags(
    aresponses: ResponsesMockServer, tags_get_response: dict[str, Any]
) -> None:
    """Test getting tags.

    Args:
    ----
        aresponses: An aresponses server.
        tags_get_response: A fixture for a tags/get response payload.

    """
    aresponses.add(
        "api.pinboard.in",
        "/v1/tags/get",
        "get",
        response=aiohttp.web_response.json_response(
            tags_get_response, content_type="text/json", status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)

        tags = await api.tag.async_get_tags()
        assert tags == {"tag1": 3, "tag2": 1, "tag3": 2}


@pytest.mark.asyncio
async def test_rename_tag(
    aresponses: ResponsesMockServer, tags_rename_response: dict[str, Any]
) -> None:
    """Test renaming a tag.

    Args:
    ----
        aresponses: An aresponses server.
        tags_rename_response: A fixture for a tags/rename response payload.

    """
    aresponses.add(
        "api.pinboard.in",
        "/v1/tags/rename",
        "get",
        response=aiohttp.web_response.json_response(
            tags_rename_response, content_type="text/json", status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)

        # A unsuccessful request will throw an exception, so if no exception is thrown,
        # we can count this as a successful test:
        await api.tag.async_rename_tag("tag1", "new-tag1")
