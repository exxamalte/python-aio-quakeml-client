"""Description."""
from __future__ import annotations

from ..consts import XML_TAG_TYPE, XML_TAG_TEXT
from .element import Element


class Description(Element):
    """Event description."""

    @property
    def type(self) -> str | None:
        """Return description's type."""
        return self._attribute_with_text([XML_TAG_TYPE])

    @property
    def text(self) -> str | None:
        """Return description's text."""
        return self._attribute_with_text([XML_TAG_TEXT])
