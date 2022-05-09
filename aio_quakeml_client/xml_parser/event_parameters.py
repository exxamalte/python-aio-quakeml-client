"""Event Parameters."""
from __future__ import annotations

import logging
from typing import List

from ..consts import XML_TAG_EVENT
from .element import Element
from .event import Event

_LOGGER = logging.getLogger(__name__)


class EventParameters(Element):
    """Represents event parameters."""

    @property
    def events(self) -> List[Event]:
        """Return the events of this feed."""
        items = self.attribute([XML_TAG_EVENT])
        entries = []
        if items and isinstance(items, list):
            for item in items:
                entries.append(Event(item))
        else:
            # A single item in the feed is not represented as an array.
            entries.append(Event(items))
        return entries
