"""Define common test utilities."""
import os

TEST_API_TOKEN = "user:abcde12345"


def load_fixture(filename) -> str:
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
