"""Origin."""
from __future__ import annotations

from ..consts import XML_TAG_LATITUDE, XML_TAG_VALUE, XML_TAG_LONGITUDE, XML_TAG_DEPTH
from .element import Element


class Origin(Element):

    @property
    def latitude(self):
        latitude = self._attribute([XML_TAG_LATITUDE])
        if latitude:
            return latitude.get(XML_TAG_VALUE)
        return None

    @property
    def longitude(self):
        longitude = self._attribute([XML_TAG_LONGITUDE])
        if longitude:
            return longitude.get(XML_TAG_VALUE)
        return None

    @property
    def depth(self):
        depth = self._attribute([XML_TAG_DEPTH])
        if depth:
            return depth.get(XML_TAG_VALUE)
        return None
