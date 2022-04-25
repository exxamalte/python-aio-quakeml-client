"""Event."""
from __future__ import annotations

import logging

from ..consts import XML_TAG_TYPE, XML_TAG_ORIGIN, XML_TAG_DESCRIPTION
from .description import Description
from .element import Element
from .origin import Origin

_LOGGER = logging.getLogger(__name__)


class Event(Element):

    @property
    def type(self):
        return self._attribute_with_text([XML_TAG_TYPE])

    @property
    def description(self) -> Description | None:
        """Event description."""
        description = self._attribute([XML_TAG_DESCRIPTION])
        if description:
            return Description(description)
        return None

    @property
    def origin(self):
        origin = self._attribute([XML_TAG_ORIGIN])
        # _LOGGER.debug("Origin: %s", origin)
        # _LOGGER.debug("Source: %s", self._source)
        if origin:
            # TODO: Could be more than 1 origin.
            # _LOGGER.debug("Event ID: %s", self.public_id)
            return Origin(origin)
