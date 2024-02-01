"""Base class for any QuakeML elements."""
from __future__ import annotations

import logging

from ..consts import XML_ATTR_PUBLICID, XML_CDATA, XML_TAG_TYPE

_LOGGER = logging.getLogger(__name__)


class Element:
    """Element."""

    def __init__(self, source: dict):
        """Initialise feed."""
        self._source = source

    def __repr__(self):
        """Return string representation of this feed item."""
        return f"<{self.__class__.__name__}({self.public_id})>"

    def attribute(self, names: list[str]) -> str | dict | None:
        """Get an attribute from this element."""
        if self._source and names:
            # Try each name, and return the first value that is not None.
            for name in names:
                value = self._source.get(name, None)
                if value:
                    return value
        return None

    def attribute_with_text(self, names: list[str]) -> str | int:
        """Get an attribute with text from this element."""
        value = self.attribute(names)
        if value and isinstance(value, dict) and XML_CDATA in value:
            # <tag attr="/some.uri">Value</tag>
            value = value.get(XML_CDATA)
        return value

    @staticmethod
    def attribute_in_structure(obj, keys: list[str]) -> str:
        """Return the attribute found under the chain of keys."""
        key: str = keys.pop(0)
        if key in obj:
            return Element.attribute_in_structure(obj[key], keys) if keys else obj[key]

    @property
    def public_id(self) -> str | None:
        """Return the public id of this element."""
        return self.attribute([XML_ATTR_PUBLICID])

    @property
    def type(self) -> str | None:
        """Return element's type."""
        return self.attribute_with_text([XML_TAG_TYPE])
