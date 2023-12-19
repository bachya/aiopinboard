"""Define typing helpers."""
from __future__ import annotations

from typing import Any

DictType = dict[str, Any]
ListDictType = list[DictType]
ResponseType = DictType | ListDictType
