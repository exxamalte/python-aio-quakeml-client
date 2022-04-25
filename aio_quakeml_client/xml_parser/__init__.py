"""XML Parser."""
from __future__ import annotations

import logging
from typing import Dict, Optional

import dateparser as dateparser
import xmltodict

from aio_quakeml_client.consts import (
    XML_TAG_Q_QUAKEML,
    XML_TAG_EVENTPARAMETERS, XML_TAG_EVENT, XML_TAG_ORIGIN, XML_TAG_LATITUDE,
    XML_TAG_VALUE, XML_TAG_LONGITUDE, XML_TAG_DEPTH, XML_TAG_TIME,
    # XML_TAG_CHANNEL,
    # XML_TAG_DC_DATE,
    # XML_TAG_FEED,
    # XML_TAG_GDACS_BBOX,
    # XML_TAG_GEO_LAT,
    # XML_TAG_GEO_LONG,
    # XML_TAG_GEORSS_POINT,
    # XML_TAG_GEORSS_POLYGON,
    # XML_TAG_GML_POS,
    # XML_TAG_GML_POS_LIST,
    # XML_TAG_HEIGHT,
    # XML_TAG_LAST_BUILD_DATE,
    # XML_TAG_PUB_DATE,
    # XML_TAG_PUBLISHED,
    # XML_TAG_RSS,
    # XML_TAG_TTL,
    # XML_TAG_UPDATED,
    # XML_TAG_WIDTH,
)
# from aio_quakeml_client.xml_parser.feed import Feed

from aio_quakeml_client.xml_parser.event_parameters import EventParameters

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAMESPACES = {
    "http://quakeml.org/xmlns/bed/1.2": None,
    "http://quakeml.org/xmlns/quakeml/1.2": "q",
}
KEYS_DATE = [
    # XML_TAG_DC_DATE,
    # XML_TAG_LAST_BUILD_DATE,
    # XML_TAG_PUB_DATE,
    # XML_TAG_PUBLISHED,
    # XML_TAG_UPDATED,
]
KEYS_FLOAT = [
    # XML_TAG_GEO_LAT, XML_TAG_GEO_LONG
]
KEYS_FLOAT_LIST = [
    # XML_TAG_GEORSS_POLYGON,
    # XML_TAG_GML_POS_LIST,
    # XML_TAG_GML_POS,
    # XML_TAG_GEORSS_POINT,
    # XML_TAG_GDACS_BBOX,
]
KEYS_CHAINS_DATE = [
    [XML_TAG_Q_QUAKEML, XML_TAG_EVENTPARAMETERS, XML_TAG_EVENT, XML_TAG_ORIGIN,
     XML_TAG_TIME, XML_TAG_VALUE],
]
KEYS_CHAINS_INT = [
    [XML_TAG_Q_QUAKEML, XML_TAG_EVENTPARAMETERS, XML_TAG_EVENT, XML_TAG_ORIGIN,
     XML_TAG_DEPTH, XML_TAG_VALUE],
]
KEY_CHAINS_FLOAT = [
    [XML_TAG_Q_QUAKEML, XML_TAG_EVENTPARAMETERS, XML_TAG_EVENT, XML_TAG_ORIGIN, XML_TAG_LATITUDE, XML_TAG_VALUE],
    [XML_TAG_Q_QUAKEML, XML_TAG_EVENTPARAMETERS, XML_TAG_EVENT, XML_TAG_ORIGIN, XML_TAG_LONGITUDE, XML_TAG_VALUE]
]


class XmlParser:
    """Built-in XML parser."""

    def __init__(self, additional_namespaces=None):
        """Initialise the XML parser."""
        self._namespaces = DEFAULT_NAMESPACES
        if additional_namespaces:
            self._namespaces.update(additional_namespaces)

    @staticmethod
    def postprocessor(path, key, value):
        """Conduct type conversion for selected keys."""
        # _LOGGER.debug("Post processing: %s, %s", path, key)
        try:
            if XmlParser._is_path_in(path, KEY_CHAINS_FLOAT):
                return key, float(value)
            if XmlParser._is_path_in(path, KEYS_CHAINS_INT):
                return key, int(value)
            if XmlParser._is_path_in(path, KEYS_CHAINS_DATE):
                return key, dateparser.parse(value)
            # if key in KEYS_DATE and value:
            #     return key, dateparser.parse(value)
            # if key in KEYS_FLOAT and value:
            #     return key, float(value)
            # if key in KEYS_FLOAT_LIST and value:
            #     point_coordinates = XmlParser._process_coordinates(value)
            #     # Return tuple of coordinates to make this conversion
            #     # compatible with parsing multiple tags of the same type and
            #     # combining all values into a single array.
            #     # If we just returned an array here, coordinates would be mixed
            #     # up like: [lat1, lon1, [lat2, lon2], [lat3, lon3]]
            #     return key, tuple(point_coordinates)
            # if key in KEYS_INT and value:
            #     return key, int(value)
        except (ValueError, TypeError) as error:
            _LOGGER.warning("Unable to process (%s/%s): %s", key, value, error)
        return key, value

    @staticmethod
    def _is_path_in(path, chains):
        """Test if the path is in any of the provided chains."""
        if path and chains:
            new_path = []
            for element in path:
                new_path.append(element[0])
            for chain in chains:
                if chain == new_path:
                    return True
        return False

    @staticmethod
    def _process_coordinates(value):
        """Turn white-space separated list of numbers into list of floats."""
        coordinate_values = value.split()
        point_coordinates = []
        for i in range(0, len(coordinate_values)):
            point_coordinates.append(float(coordinate_values[i]))
        return point_coordinates

    def parse(self, xml) -> Optional[EventParameters]:
        """Parse the provided xml."""
        if xml:
            parsed_dict = xmltodict.parse(
                xml,
                process_namespaces=True,
                namespaces=self._namespaces,
                postprocessor=XmlParser.postprocessor,
            )
            if XML_TAG_Q_QUAKEML in parsed_dict:
                return XmlParser._create_feed_from_quakeml(parsed_dict)
        return None

    @staticmethod
    def _create_feed_from_quakeml(parsed_dict: Dict) -> Optional[EventParameters]:
        """Create feed from provided RSS data."""
        quakeml = parsed_dict.get(XML_TAG_Q_QUAKEML)
        print(quakeml)
        if XML_TAG_EVENTPARAMETERS in quakeml:
            events = quakeml.get(XML_TAG_EVENTPARAMETERS)
            return EventParameters(events)
        else:
            _LOGGER.warning(
                "Invalid structure: Missing top level element %s", XML_TAG_Q_QUAKEML
            )
            return None
