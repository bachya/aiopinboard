"""Define helpers related to bookmarks."""
from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Bookmark:  # pylint: disable=too-many-instance-attributes
    """Define a representation of a Pinboard bookmark."""

    hash: str
    href: str
    title: str
    description: str
    last_modified: datetime
    tags: List[str]
    unread: bool
    shared: bool
