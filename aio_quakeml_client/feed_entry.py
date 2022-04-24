"""Feed Entry."""
import logging
import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Tuple, Type

from .consts import CUSTOM_ATTRIBUTE
from .origin_distance_helper import OriginDistanceHelper
from .xml_parser.event import Event
from .xml_parser.geometry import Geometry, Point

_LOGGER = logging.getLogger(__name__)

DEFAULT_FEATURES = [
    Point,
    # Polygon, BoundingBox
]


class FeedEntry(ABC):
    """Feed entry base class."""

    def __init__(self, home_coordinates: Tuple[float, float], quakeml_event: Event):
        """Initialise this feed entry."""
        self._home_coordinates = home_coordinates
        self._quakeml_event = quakeml_event

    def __repr__(self):
        """Return string representation of this entry."""
        return "<{}(id={})>".format(self.__class__.__name__, self.external_id)

    @property
    def features(self) -> List[Type[Geometry]]:
        """Return the list of geometry types that this feed entry supports."""
        return DEFAULT_FEATURES

    @property
    def geometries(self) -> Optional[List[Geometry]]:
        """Return all geometries of this entry."""
        if self._quakeml_event and self._quakeml_event.origin:
            return [Point(self._quakeml_event.origin.latitude, self._quakeml_event.origin.longitude)]
            # # Return all geometries that are of type defined in features.
            # return list(
            #     filter(lambda x: type(x) in self.features, self._quakeml_event.origin)
            # )
        return None

    @property
    def coordinates(self) -> Optional[Tuple[float, float]]:
        """Return the best coordinates (latitude, longitude) of this entry."""
        # This looks for the first point in the list of geometries. If there
        # is no point then return the first entry.
        if self.geometries and len(self.geometries) >= 1:
            for entry in self.geometries:
                if isinstance(entry, Point):
                    return OriginDistanceHelper.extract_coordinates(entry)
            # No point found.
            return OriginDistanceHelper.extract_coordinates(self.geometries[0])
        return None

    @property
    def external_id(self) -> Optional[str]:
        """Return the external id of this entry."""
        if self._quakeml_event:
            external_id = self._quakeml_event.public_id
            if not external_id:
                external_id = self.title
            if not external_id:
                # Use geometry as ID as a fallback.
                external_id = hash(self.coordinates)
            return external_id
        return None

    def _search_in_external_id(self, regexp) -> Optional[str]:
        """Find a sub-string in the entry's external id."""
        if self.external_id:
            match = re.search(regexp, self.external_id)
            if match:
                return match.group(CUSTOM_ATTRIBUTE)
        return None

    @property
    def title(self) -> Optional[str]:
        """Return the title of this entry."""
        if self._quakeml_event:
            return self._quakeml_event.title
        return None

    def _search_in_title(self, regexp):
        """Find a sub-string in the entry's title."""
        if self.title:
            match = re.search(regexp, self.title)
            if match:
                return match.group(CUSTOM_ATTRIBUTE)
        return None

    # @property
    # def category(self) -> Optional[str]:
    #     """Return the category of this entry."""
    #     if (
    #         self._quakeml_event
    #         and self._quakeml_event.category
    #         and isinstance(self._quakeml_event.category, list)
    #     ):
    #         # To keep this simple, just return the first category.
    #         return self._quakeml_event.category[0]
    #     return None

    @property
    @abstractmethod
    def attribution(self) -> Optional[str]:
        """Return the attribution of this entry."""
        return None

    @property
    def distance_to_home(self) -> float:
        """Return the distance in km of this entry to the home coordinates."""
        # This goes through all geometries and reports back the closest
        # distance to any of them.
        distance = float("inf")
        if self.geometries and len(self.geometries) >= 1:
            for geometry in self.geometries:
                distance = min(
                    distance,
                    OriginDistanceHelper.distance_to_geometry(
                        self._home_coordinates, geometry
                    ),
                )
        return distance

    @property
    def description(self) -> Optional[str]:
        """Return the description of this entry."""
        if self._quakeml_event and self._quakeml_event.description:
            return self._quakeml_event.description
        return None

    @property
    def published(self) -> Optional[datetime]:
        """Return the published date of this entry."""
        if self._quakeml_event:
            return self._quakeml_event.published_date
        return None

    @property
    def updated(self) -> Optional[datetime]:
        """Return the updated date of this entry."""
        if self._quakeml_event:
            return self._quakeml_event.updated_date
        return None

    def _search_in_description(self, regexp):
        """Find a sub-string in the entry's description."""
        if self.description:
            match = re.search(regexp, self.description)
            if match:
                return match.group(CUSTOM_ATTRIBUTE)
        return None

    @staticmethod
    def _string2boolean(value: str) -> bool:
        """Convert value to boolean."""
        return isinstance(value, str) and value.strip().lower() in {"true", "yes", "1"}
