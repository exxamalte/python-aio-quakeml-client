"""QuakeML Distance Helper."""
import logging
from typing import Optional, Tuple

from haversine import haversine

from .xml_parser.geometry import Geometry, Point

_LOGGER = logging.getLogger(__name__)


class OriginDistanceHelper:
    """Helper to calculate distances between GeoRSS geometries."""

    def __init__(self):
        """Initialize the geo distance helper."""
        pass

    @staticmethod
    def extract_coordinates(geometry: Geometry) -> Optional[Tuple[float, float]]:
        """Extract the best coordinates from the feature for display."""
        latitude = longitude = None
        if isinstance(geometry, Point):
            # Just extract latitude and longitude directly.
            latitude, longitude = geometry.latitude, geometry.longitude
        else:
            _LOGGER.debug("Not implemented: %s", type(geometry))
        return latitude, longitude

    @staticmethod
    def distance_to_geometry(
        home_coordinates: Tuple[float, float], geometry: Geometry
    ) -> float:
        """Calculate the distance between home coordinates and geometry."""
        distance = float("inf")
        if isinstance(geometry, Point):
            distance = OriginDistanceHelper._distance_to_point(
                home_coordinates, geometry
            )
        else:
            _LOGGER.debug("Not implemented: %s", type(geometry))
        return distance

    @staticmethod
    def _distance_to_point(
        home_coordinates: Tuple[float, float], point: Point
    ) -> float:
        """Calculate the distance between home coordinates and the point."""
        # Swap coordinates to match: (latitude, longitude).
        return OriginDistanceHelper._distance_to_coordinates(
            home_coordinates, (point.latitude, point.longitude)
        )

    @staticmethod
    def _distance_to_coordinates(
        home_coordinates: Tuple[float, float], coordinates: Tuple[float, float]
    ) -> float:
        """Calculate the distance between home coordinates and the
        coordinates."""
        # Expecting coordinates in format: (latitude, longitude).
        return haversine(coordinates, home_coordinates)

    @staticmethod
    def _distance_to_edge(
        home_coordinates: Tuple[float, float], edge: Tuple[Point, Point]
    ) -> float:
        """Calculate distance between home coordinates and provided edge."""
        perpendicular_point = OriginDistanceHelper._perpendicular_point(
            edge, Point(home_coordinates[0], home_coordinates[1])
        )
        # If there is a perpendicular point on the edge -> calculate distance.
        # If there isn't, then the distance to the end points of the edge will
        # need to be considered separately.
        if perpendicular_point:
            distance = OriginDistanceHelper._distance_to_point(
                home_coordinates, perpendicular_point
            )
            _LOGGER.debug(
                "Distance between %s and %s: %s", home_coordinates, edge, distance
            )
            return distance
        return float("inf")

    @staticmethod
    def _perpendicular_point(
        edge: Tuple[Point, Point], point: Point
    ) -> Optional[Point]:
        """Find a perpendicular point on the edge to the provided point."""
        a, b = edge
        # Safety check: a and b can't be an edge if they are the same point.
        if a == b:
            return None
        px = point.longitude
        py = point.latitude
        ax = a.longitude
        ay = a.latitude
        bx = b.longitude
        by = b.latitude
        # Alter longitude to cater for 180 degree crossings.
        if px < 0:
            px += 360.0
        if ax < 0:
            ax += 360.0
        if bx < 0:
            bx += 360.0
        if ay > by or ax > bx:
            ax, ay, bx, by = bx, by, ax, ay
        dx = abs(bx - ax)
        dy = abs(by - ay)
        shortest_length = ((dx * (px - ax)) + (dy * (py - ay))) / (
            (dx * dx) + (dy * dy)
        )
        rx = ax + dx * shortest_length
        ry = ay + dy * shortest_length
        if bx >= rx >= ax and by >= ry >= ay:
            if rx > 180:
                # Correct longitude.
                rx -= 360.0
            return Point(ry, rx)
        return None
