"""Test note API endpoints."""
from datetime import datetime

import pytest
import pytz
from aiohttp import ClientSession
from aresponses import ResponsesMockServer

from aiopinboard import API
from aiopinboard.note import Note
from tests.common import TEST_API_TOKEN, load_fixture


@pytest.mark.asyncio
async def test_get_notes(aresponses: ResponsesMockServer) -> None:
    """Test getting notes.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "api.pinboard.in",
        "/v1/notes/list",
        "get",
        aresponses.Response(text=load_fixture("notes_get_response.xml"), status=200),
    )

    async with ClientSession() as session:
        api = API(TEST_API_TOKEN, session=session)

        notes = await api.note.async_get_notes()
        assert len(notes) == 1
        assert notes[0] == Note(
            "xxxxxxxxxxxxxxxxxxxx",
            "Test",
            "xxxxxxxxxxxxxxxxxxxx",
            pytz.utc.localize(datetime(2020, 9, 6, 5, 59, 47)),
            pytz.utc.localize(datetime(2020, 9, 6, 5, 59, 47)),
            14,
        )
