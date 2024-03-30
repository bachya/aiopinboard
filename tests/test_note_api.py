"""Test note API endpoints."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import aiohttp
from aresponses import ResponsesMockServer
import pytest

from aiopinboard import API
from aiopinboard.note import Note
from tests.common import TEST_API_TOKEN


@pytest.mark.asyncio()
async def test_get_notes(
    aresponses: ResponsesMockServer, notes_get_response: dict[str, Any]
) -> None:
    """Test getting notes.

    Args:
    ----
        aresponses: An aresponses server.
        notes_get_response: A notes get response.

    """
    aresponses.add(
        "api.pinboard.in",
        "/v1/notes/list",
        "get",
        response=aiohttp.web_response.json_response(
            notes_get_response, content_type="text/json", status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)

        notes = await api.note.async_get_notes()
        assert len(notes) == 1
        assert notes[0] == Note(
            "xxxxxxxxxxxxxxxxxxxx",
            "Test",
            "xxxxxxxxxxxxxxxxxxxx",
            datetime(2020, 9, 6, 5, 59, 47, tzinfo=timezone.utc),
            datetime(2020, 9, 6, 5, 59, 47, tzinfo=timezone.utc),
            14,
        )
