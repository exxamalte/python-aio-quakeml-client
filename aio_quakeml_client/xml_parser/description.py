"""Description."""
from ..consts import XML_TAG_TYPE, XML_TAG_TEXT
from .element import Element


class Description(Element):

    @property
    def type(self):
        return self._attribute_with_text([XML_TAG_TYPE])

    @property
    def text(self):
        return self._attribute_with_text([XML_TAG_TEXT])
