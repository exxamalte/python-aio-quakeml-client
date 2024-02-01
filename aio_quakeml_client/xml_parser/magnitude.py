"""Magnitude."""
from __future__ import annotations

from ..consts import XML_TAG_MAG, XML_TAG_STATIONCOUNT, XML_TAG_VALUE
from .element import Element


class Magnitude(Element):
    """Event magnitude."""

    @property
    def mag(self) -> float | None:
        """Return magnitude value."""
        time: dict | None = self.attribute([XML_TAG_MAG])
        if time:
            return time.get(XML_TAG_VALUE)
        return None

    @property
    def station_count(self) -> int | None:
        """Return number of used stations for this magnitude computation."""
        return self.attribute_with_text([XML_TAG_STATIONCOUNT])
