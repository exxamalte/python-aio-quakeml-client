"""XML Parser."""
from __future__ import annotations

import logging
from typing import Dict, Optional

import dateparser as dateparser
import xmltodict

from aio_quakeml_client.consts import (
    XML_TAG_CREATIONINFO,
    XML_TAG_CREATIONTIME,
    XML_TAG_DEPTH,
    XML_TAG_EVENT,
    XML_TAG_EVENTPARAMETERS,
    XML_TAG_LATITUDE,
    XML_TAG_LONGITUDE,
    XML_TAG_MAG,
    XML_TAG_MAGNITUDE,
    XML_TAG_ORIGIN,
    XML_TAG_Q_QUAKEML,
    XML_TAG_STATIONCOUNT,
    XML_TAG_TIME,
    XML_TAG_VALUE,
)
from aio_quakeml_client.xml_parser.event_parameters import EventParameters

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAMESPACES = {
    "http://quakeml.org/xmlns/bed/1.2": None,
    "http://quakeml.org/xmlns/quakeml/1.2": "q",
}
KEYS_CHAINS_DATE = [
    [
        XML_TAG_Q_QUAKEML,
        XML_TAG_EVENTPARAMETERS,
        XML_TAG_EVENT,
        XML_TAG_ORIGIN,
        XML_TAG_TIME,
        XML_TAG_VALUE,
    ],
    [
        XML_TAG_Q_QUAKEML,
        XML_TAG_EVENTPARAMETERS,
        XML_TAG_EVENT,
        XML_TAG_CREATIONINFO,
        XML_TAG_CREATIONTIME,
    ],
]
KEYS_CHAINS_INT = [
    [
        XML_TAG_Q_QUAKEML,
        XML_TAG_EVENTPARAMETERS,
        XML_TAG_EVENT,
        XML_TAG_ORIGIN,
        XML_TAG_DEPTH,
        XML_TAG_VALUE,
    ],
    [
        XML_TAG_Q_QUAKEML,
        XML_TAG_EVENTPARAMETERS,
        XML_TAG_EVENT,
        XML_TAG_MAGNITUDE,
        XML_TAG_STATIONCOUNT,
    ],
]
KEY_CHAINS_FLOAT = [
    [
        XML_TAG_Q_QUAKEML,
        XML_TAG_EVENTPARAMETERS,
        XML_TAG_EVENT,
        XML_TAG_ORIGIN,
        XML_TAG_LATITUDE,
        XML_TAG_VALUE,
    ],
    [
        XML_TAG_Q_QUAKEML,
        XML_TAG_EVENTPARAMETERS,
        XML_TAG_EVENT,
        XML_TAG_ORIGIN,
        XML_TAG_LONGITUDE,
        XML_TAG_VALUE,
    ],
    [
        XML_TAG_Q_QUAKEML,
        XML_TAG_EVENTPARAMETERS,
        XML_TAG_EVENT,
        XML_TAG_MAGNITUDE,
        XML_TAG_MAG,
        XML_TAG_VALUE,
    ],
]


class XmlParser:
    """Built-in XML parser."""

    def __init__(self, additional_namespaces: Dict = None):
        """Initialise the XML parser."""
        self._namespaces = DEFAULT_NAMESPACES
        if additional_namespaces:
            self._namespaces.update(additional_namespaces)

    @staticmethod
    def postprocessor(path, key, value):
        """Conduct type conversion for selected keys."""
        try:
            if XmlParser._is_path_in(path, KEY_CHAINS_FLOAT):
                return key, float(value)
            if XmlParser._is_path_in(path, KEYS_CHAINS_INT):
                return key, int(value)
            if XmlParser._is_path_in(path, KEYS_CHAINS_DATE):
                return key, dateparser.parse(
                    value,
                    settings={"TIMEZONE": "UTC", "RETURN_AS_TIMEZONE_AWARE": True},
                )
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
        if XML_TAG_EVENTPARAMETERS in quakeml:
            events = quakeml.get(XML_TAG_EVENTPARAMETERS)
            return EventParameters(events)
        else:
            _LOGGER.warning(
                "Invalid structure: Missing top level element %s", XML_TAG_Q_QUAKEML
            )
            return None
