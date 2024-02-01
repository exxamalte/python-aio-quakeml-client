"""Event."""
from __future__ import annotations

import logging

from ..consts import (
    XML_TAG_CREATIONINFO,
    XML_TAG_DESCRIPTION,
    XML_TAG_MAGNITUDE,
    XML_TAG_ORIGIN,
)
from .creation_info import CreationInfo
from .description import Description
from .element import Element
from .magnitude import Magnitude
from .origin import Origin

_LOGGER = logging.getLogger(__name__)


class Event(Element):
    """Event."""

    @property
    def description(self) -> Description | None:
        """Event description."""
        description: dict | None = self.attribute([XML_TAG_DESCRIPTION])
        if description:
            return Description(description)
        return None

    @property
    def origin(self) -> Origin | None:
        """First defined origin."""
        if self.origins:
            return self.origins[0]
        return None

    @property
    def origins(self) -> list[Origin] | None:
        """Origins defined for this event."""
        origins: dict = self.attribute([XML_TAG_ORIGIN])
        entries: list = []
        if origins:
            if isinstance(origins, list):
                for origin in origins:
                    entries.append(Origin(origin))
            else:
                entries.append(Origin(origins))
        return entries

    @property
    def magnitude(self) -> Magnitude | None:
        """First defined magnitude."""
        if self.magnitudes:
            return self.magnitudes[0]
        return None

    @property
    def magnitudes(self) -> list[Magnitude] | None:
        """Magnitudes defined for this event."""
        magnitudes: dict | None = self.attribute([XML_TAG_MAGNITUDE])
        entries: list = []
        if magnitudes:
            if isinstance(magnitudes, list):
                for magnitude in magnitudes:
                    entries.append(Magnitude(magnitude))
            else:
                entries.append(Magnitude(magnitudes))
        return entries

    @property
    def creation_info(self) -> CreationInfo | None:
        """Creation info about this event."""
        creation_info: dict | None = self.attribute([XML_TAG_CREATIONINFO])
        if creation_info:
            return CreationInfo(creation_info)
        return None
