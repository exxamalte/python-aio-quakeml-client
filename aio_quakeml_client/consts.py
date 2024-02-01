"""Constants for feeds and feed entries."""
from typing import Final

ATTR_ATTRIBUTION: Final = "attribution"

CUSTOM_ATTRIBUTE: Final = "custom_attribute"

DEFAULT_REQUEST_TIMEOUT: Final = 10

UPDATE_OK: Final = "OK"
UPDATE_OK_NO_DATA: Final = "OK_NO_DATA"
UPDATE_ERROR: Final = "ERROR"

XML_ATTR_PUBLICID: Final = "@publicID"

XML_CDATA: Final = "#text"

XML_TAG_Q_QUAKEML: Final = "q:quakeml"
XML_TAG_AGENCYID: Final = "agencyID"
XML_TAG_AUTHOR: Final = "author"
XML_TAG_CREATIONINFO: Final = "creationInfo"
XML_TAG_CREATIONTIME: Final = "creationTime"
XML_TAG_DEPTH: Final = "depth"
XML_TAG_DEPTHTYPE: Final = "depthType"
XML_TAG_DESCRIPTION: Final = "description"
XML_TAG_EVENT: Final = "event"
XML_TAG_EVALUATIONMODE: Final = "evaluationMode"
XML_TAG_EVALUATIONSTATUS: Final = "evaluationStatus"
XML_TAG_EVENTPARAMETERS: Final = "eventParameters"
XML_TAG_LATITUDE: Final = "latitude"
XML_TAG_LONGITUDE: Final = "longitude"
XML_TAG_MAG: Final = "mag"
XML_TAG_MAGNITUDE: Final = "magnitude"
XML_TAG_ORIGIN: Final = "origin"
XML_TAG_STATIONCOUNT: Final = "stationCount"
XML_TAG_TEXT: Final = "text"
XML_TAG_TIME: Final = "time"
XML_TAG_TYPE: Final = "type"
XML_TAG_VALUE: Final = "value"
