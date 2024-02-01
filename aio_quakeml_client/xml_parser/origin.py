"""Origin."""
from __future__ import annotations

from datetime import datetime

from ..consts import (
    XML_TAG_DEPTH,
    XML_TAG_DEPTHTYPE,
    XML_TAG_EVALUATIONMODE,
    XML_TAG_EVALUATIONSTATUS,
    XML_TAG_LATITUDE,
    XML_TAG_LONGITUDE,
    XML_TAG_TIME,
    XML_TAG_VALUE,
)
from .element import Element


class Origin(Element):
    """Focal time and geographical location of an earthquake hypocenter."""

    @property
    def latitude(self) -> float | None:
        """Return the hypocenter latitude."""
        latitude: dict | None = self.attribute([XML_TAG_LATITUDE])
        if latitude:
            return latitude.get(XML_TAG_VALUE)
        return None

    @property
    def longitude(self) -> float | None:
        """Return the hypocenter longitude."""
        longitude: dict | None = self.attribute([XML_TAG_LONGITUDE])
        if longitude:
            return longitude.get(XML_TAG_VALUE)
        return None

    @property
    def depth(self) -> float | None:
        """Return depth of hypocenter with respect to the nominal sea level."""
        depth: dict | None = self.attribute([XML_TAG_DEPTH])
        if depth:
            return depth.get(XML_TAG_VALUE)
        return None

    @property
    def depth_type(self) -> str | None:
        """Return type of depth determination."""
        return self.attribute([XML_TAG_DEPTHTYPE])

    @property
    def time(self) -> datetime | None:
        """Return focal time."""
        time: dict | None = self.attribute([XML_TAG_TIME])
        if time:
            return time.get(XML_TAG_VALUE)
        return None

    @property
    def evaluation_mode(self) -> str | None:
        """Return mode of evaluation ."""
        return self.attribute_with_text([XML_TAG_EVALUATIONMODE])

    @property
    def evaluation_status(self) -> str | None:
        """Return status of evaluation ."""
        return self.attribute_with_text([XML_TAG_EVALUATIONSTATUS])
