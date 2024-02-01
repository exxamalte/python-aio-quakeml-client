"""Feed Entry."""
from __future__ import annotations

import logging
import re
from abc import ABC, abstractmethod

from haversine import haversine

from .consts import CUSTOM_ATTRIBUTE
from .xml_parser.creation_info import CreationInfo
from .xml_parser.event import Event
from .xml_parser.magnitude import Magnitude
from .xml_parser.origin import Origin

_LOGGER = logging.getLogger(__name__)


class FeedEntry(ABC):
    """Feed entry base class."""

    def __init__(self, home_coordinates: tuple[float, float], quakeml_event: Event):
        """Initialise this feed entry."""
        self._home_coordinates: tuple[float, float] = home_coordinates
        self._quakeml_event: Event = quakeml_event

    def __repr__(self):
        """Return string representation of this entry."""
        return f"<{self.__class__.__name__}(id={self.external_id})>"

    @property
    def coordinates(self) -> tuple[float, float] | None:
        """Return the coordinates (latitude, longitude) of this entry."""
        if self.origin and self.origin.latitude and self.origin.longitude:
            return self.origin.latitude, self.origin.longitude
        return None

    @property
    def external_id(self) -> str | None:
        """Return the external id of this entry."""
        if self._quakeml_event:
            external_id: str | None = self._quakeml_event.public_id
            if not external_id:
                # Use geometry as ID as a fallback.
                external_id = str(hash(self.coordinates))
            return external_id
        return None

    def _search_in_external_id(self, regexp) -> str | None:
        """Find a sub-string in the entry's external id."""
        if self.external_id:
            match = re.search(regexp, self.external_id)
            if match:
                return match.group(CUSTOM_ATTRIBUTE)
        return None

    @property
    @abstractmethod
    def attribution(self) -> str | None:
        """Return the attribution of this entry."""
        return None

    @property
    def distance_to_home(self) -> float:
        """Return the distance in km of this entry to the home coordinates."""
        distance: float = float("inf")
        if self.coordinates:
            # Expecting coordinates in format: (latitude, longitude).
            return haversine(self.coordinates, self._home_coordinates)
        return distance

    @property
    def type(self) -> str | None:
        """Return entry's type."""
        if self._quakeml_event:
            return self._quakeml_event.type
        return None

    @property
    def description(self) -> str | None:
        """Return the description of this entry."""
        if self._quakeml_event and self._quakeml_event.description:
            if self._quakeml_event.description.type:
                return f"{self._quakeml_event.description.type.capitalize()}: {self._quakeml_event.description.text}"
            else:
                return self._quakeml_event.description.text
        return None

    @property
    def creation_info(self) -> CreationInfo | None:
        """Return creation info."""
        if self._quakeml_event:
            return self._quakeml_event.creation_info
        return None

    @property
    def magnitude(self) -> Magnitude | None:
        """Return magnitude."""
        if self._quakeml_event:
            return self._quakeml_event.magnitude
        return None

    @property
    def origin(self) -> Origin | None:
        """Return origin."""
        if self._quakeml_event:
            return self._quakeml_event.origin
        return None
