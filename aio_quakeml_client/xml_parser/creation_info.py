"""Creation info."""
from __future__ import annotations

from ..consts import XML_TAG_AGENCYID, XML_TAG_AUTHOR, XML_TAG_CREATIONTIME
from .element import Element


class CreationInfo(Element):
    """Creation metadata."""

    @property
    def agency_id(self) -> str | None:
        """Return designation of agency that published a resource."""
        return self.attribute_with_text([XML_TAG_AGENCYID])

    @property
    def author(self) -> str | None:
        """Return name describing the author of a resource."""
        return self.attribute_with_text([XML_TAG_AUTHOR])

    @property
    def creation_time(self) -> str | None:
        """Return time of creation of a resource."""
        return self.attribute_with_text([XML_TAG_CREATIONTIME])
