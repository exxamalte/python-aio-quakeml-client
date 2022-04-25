"""Origin."""
from __future__ import annotations

from ..consts import XML_TAG_LATITUDE, XML_TAG_VALUE, XML_TAG_LONGITUDE, XML_TAG_DEPTH, \
    XML_TAG_DEPTHTYPE
from .element import Element


class Origin(Element):
    """Focal time and geographical location of an earthquake hypocenter."""

    @property
    def latitude(self) -> float | None:
        """Return the hypocenter latitude."""
        latitude = self._attribute([XML_TAG_LATITUDE])
        if latitude:
            return latitude.get(XML_TAG_VALUE)
        return None

    @property
    def longitude(self) -> float | None:
        """Return the hypocenter longitude."""
        longitude = self._attribute([XML_TAG_LONGITUDE])
        if longitude:
            return longitude.get(XML_TAG_VALUE)
        return None

    @property
    def depth(self) -> float | None:
        """Return depth of hypocenter with respect to the nominal sea level."""
        depth = self._attribute([XML_TAG_DEPTH])
        if depth:
            return depth.get(XML_TAG_VALUE)
        return None

    @property
    def depth_type(self) -> str | None:
        """Return type of depth determination."""
        depth = self._attribute([XML_TAG_DEPTHTYPE])
        if depth:
            return depth.get(XML_TAG_DEPTHTYPE).capitalize()
        return None
