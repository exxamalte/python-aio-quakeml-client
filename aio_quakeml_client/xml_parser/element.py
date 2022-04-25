"""Base class for any QuakeML elements."""
from __future__ import annotations

from typing import List, Optional, Dict

from ..consts import XML_ATTR_PUBLICID, XML_CDATA


class Element:

    def __init__(self, source: Dict):
        """Initialise feed."""
        self._source = source

    def __repr__(self):
        """Return string representation of this feed item."""
        return "<{}({})>".format(self.__class__.__name__, self.public_id)

    def _attribute(self, names: List[str]) -> Optional:
        """Get an attribute from this element."""
        if self._source and names:
            # Try each name, and return the first value that is not None.
            for name in names:
                value = self._source.get(name, None)
                if value:
                    return value
        return None

    def _attribute_with_text(self, names: List[str]) -> Optional:
        """Get an attribute with text from this element."""
        value = self._attribute(names)
        if value and isinstance(value, dict) and XML_CDATA in value:
            # <tag attr="/some.uri">Value</tag>
            value = value.get(XML_CDATA)
        return value

    @staticmethod
    def _attribute_in_structure(obj, keys: List[str]) -> Optional:
        """Return the attribute found under the chain of keys."""
        key = keys.pop(0)
        if key in obj:
            return (
                Element._attribute_in_structure(obj[key], keys)
                if keys
                else obj[key]
            )

    @property
    def public_id(self) -> str | None:
        """Return the public id of this feed."""
        return self._attribute([XML_ATTR_PUBLICID])
