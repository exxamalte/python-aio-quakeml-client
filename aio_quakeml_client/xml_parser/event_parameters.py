"""Event Parameters."""
import logging

from ..consts import XML_TAG_EVENT
from .element import Element
from .event import Event

_LOGGER = logging.getLogger(__name__)


class EventParameters(Element):
    """Represents event parameters."""

    @property
    def events(self):
        """Return the events of this feed."""
        _LOGGER.debug("Event Parameters Source: %s", self._source)
        items = self._attribute([XML_TAG_EVENT])
        _LOGGER.debug("Event Parameters: %s", items)
        entries = []
        if items and isinstance(items, list):
            for item in items:
                entries.append(Event(item))
        else:
            # A single item in the feed is not represented as an array.
            entries.append(Event(items))
        return entries
