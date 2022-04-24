"""Event."""
from ..consts import XML_TAG_TYPE, XML_TAG_ORIGIN, XML_TAG_DESCRIPTION
from .description import Description
from .element import Element
from .origin import Origin


class Event(Element):

    @property
    def type(self):
        return self._attribute_with_text([XML_TAG_TYPE])

    @property
    def description(self):
        """Event description."""
        description = self._attribute([XML_TAG_DESCRIPTION])
        if description:
            return Description(description)

    @property
    def origin(self):
        origin = self._attribute([XML_TAG_ORIGIN])
        if origin:
            # TODO: Could be more than 1 origin.
            return Origin(origin)
