"""Define dynamic test fixtures."""
import json
from typing import Any, cast

import pytest

from tests.common import load_fixture


@pytest.fixture(name="error_response", scope="session")
def error_response_fixture() -> dict[str, Any]:
    """Return a fixture for a failed auth response payload."""
    return cast(dict[str, Any], json.loads(load_fixture("error_response.json")))


@pytest.fixture(name="notes_get_response", scope="session")
def notes_get_response_fixture() -> dict[str, Any]:
    """Return a fixture for a notes response payload."""
    return cast(dict[str, Any], json.loads(load_fixture("notes_get_response.json")))


@pytest.fixture(name="posts_add_response", scope="session")
def posts_add_response_fixture() -> dict[str, Any]:
    """Return a fixture for a posts/add response payload."""
    return cast(dict[str, Any], json.loads(load_fixture("posts_add_response.json")))


@pytest.fixture(name="posts_all_response", scope="session")
def posts_all_response_fixture() -> dict[str, Any]:
    """Return a fixture for a posts/all response payload."""
    return cast(dict[str, Any], json.loads(load_fixture("posts_all_response.json")))


@pytest.fixture(name="posts_dates_response", scope="session")
def posts_dates_response_fixture() -> dict[str, Any]:
    """Return a fixture for a posts/dates response payload."""
    return cast(dict[str, Any], json.loads(load_fixture("posts_dates_response.json")))


@pytest.fixture(name="posts_delete_response", scope="session")
def posts_delete_response_fixture() -> dict[str, Any]:
    """Return a fixture for a posts/delete response payload."""
    return cast(dict[str, Any], json.loads(load_fixture("posts_delete_response.json")))


@pytest.fixture(name="posts_get_empty_response", scope="session")
def posts_get_empty_response_fixture() -> dict[str, Any]:
    """Return a fixture for a posts/get response payload."""
    return cast(
        dict[str, Any], json.loads(load_fixture("posts_get_empty_response.json"))
    )


@pytest.fixture(name="posts_get_response", scope="session")
def posts_get_response_fixture() -> dict[str, Any]:
    """Return a fixture for a posts/get response payload."""
    return cast(dict[str, Any], json.loads(load_fixture("posts_get_response.json")))


@pytest.fixture(name="posts_recent_response", scope="session")
def posts_recent_response_fixture() -> dict[str, Any]:
    """Return a fixture for a posts/recent response payload."""
    return cast(dict[str, Any], json.loads(load_fixture("posts_recent_response.json")))


@pytest.fixture(name="posts_suggest_response", scope="session")
def posts_suggest_response_fixture() -> dict[str, Any]:
    """Return a fixture for a posts/suggest response payload."""
    return cast(dict[str, Any], json.loads(load_fixture("posts_suggest_response.json")))


@pytest.fixture(name="posts_update_response", scope="session")
def posts_update_response_fixture() -> dict[str, Any]:
    """Return a fixture for a posts/update response payload."""
    return cast(dict[str, Any], json.loads(load_fixture("posts_update_response.json")))


@pytest.fixture(name="tags_delete_response", scope="session")
def tags_delete_response_fixture() -> dict[str, Any]:
    """Return a fixture for a tags/delete response payload."""
    return cast(dict[str, Any], json.loads(load_fixture("tags_delete_response.json")))


@pytest.fixture(name="tags_get_response", scope="session")
def tags_get_response_fixture() -> dict[str, Any]:
    """Return a fixture for a tags/get response payload."""
    return cast(dict[str, Any], json.loads(load_fixture("tags_get_response.json")))


@pytest.fixture(name="tags_rename_response", scope="session")
def tags_rename_response_fixture() -> dict[str, Any]:
    """Return a fixture for a tags/rename response payload."""
    return cast(dict[str, Any], json.loads(load_fixture("tags_rename_response.json")))
