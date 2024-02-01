"""Event Parameters."""
from __future__ import annotations

import logging

from ..consts import XML_TAG_EVENT
from .element import Element
from .event import Event

_LOGGER = logging.getLogger(__name__)


class EventParameters(Element):
    """Represents event parameters."""

    @property
    def events(self) -> list[Event]:
        """Return the events of this feed."""
        items: dict | None = self.attribute([XML_TAG_EVENT])
        entries: list = []
        if items and isinstance(items, list):
            for item in items:
                entries.append(Event(item))
        else:
            # A single item in the feed is not represented as an array.
            entries.append(Event(items))
        return entries
