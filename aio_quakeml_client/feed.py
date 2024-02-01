"""QuakeML Feed."""
from __future__ import annotations

import asyncio
import codecs
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generic, TypeVar

import aiohttp
from aiohttp import ClientSession, client_exceptions
from pyexpat import ExpatError

from .consts import DEFAULT_REQUEST_TIMEOUT, UPDATE_ERROR, UPDATE_OK, UPDATE_OK_NO_DATA
from .feed_entry import FeedEntry
from .xml_parser import EventParameters, XmlParser
from .xml_parser.event import Event

_LOGGER = logging.getLogger(__name__)

T_FEED_ENTRY = TypeVar("T_FEED_ENTRY", bound=FeedEntry)


class QuakeMLFeed(Generic[T_FEED_ENTRY], ABC):
    """QuakeML feed base class."""

    def __init__(
        self,
        websession: ClientSession,
        home_coordinates: tuple[float, float],
        url: str = None,
        filter_radius: float = None,
        filter_minimum_magnitude: float = None,
    ):
        """Initialise this service."""
        self._websession: ClientSession = websession
        self._home_coordinates: tuple[float, float] = home_coordinates
        self._url: str | None = url
        self._filter_radius: float | None = filter_radius
        self._filter_minimum_magnitude: float | None = filter_minimum_magnitude
        self._last_timestamp: datetime | None = None

    def __repr__(self):
        """Return string representation of this feed."""
        return "<{}(home={}, url={}, radius={}, magnitude={})>".format(
            self.__class__.__name__,
            self._home_coordinates,
            self._fetch_url(),
            self._filter_radius,
            self._filter_minimum_magnitude,
        )

    @abstractmethod
    def _new_entry(
        self,
        home_coordinates: tuple[float, float],
        event: Event,
        global_data: dict | None,
    ) -> T_FEED_ENTRY:
        """Generate a new entry."""
        pass

    def _client_session_timeout(self) -> int:
        """Define client session timeout in seconds. Override if necessary."""
        return DEFAULT_REQUEST_TIMEOUT

    def _additional_namespaces(self) -> dict | None:
        """Provide additional namespaces, relevant for this feed."""
        pass

    async def update(self) -> tuple[str, list[T_FEED_ENTRY] | None]:
        """Update from external source and return filtered entries."""
        status, quakeml_data = await self._fetch()
        if status == UPDATE_OK:
            if quakeml_data:
                entries: list = []
                global_data: dict | None = self._extract_from_feed(quakeml_data)
                # Extract data from feed entries.
                for event in quakeml_data.events:
                    entries.append(
                        self._new_entry(self._home_coordinates, event, global_data)
                    )
                filtered_entries: list[T_FEED_ENTRY] = self._filter_entries(entries)
                self._last_timestamp = self._extract_last_timestamp(filtered_entries)
                return UPDATE_OK, filtered_entries
            else:
                # Should not happen.
                return UPDATE_OK, None
        elif status == UPDATE_OK_NO_DATA:
            # Happens for example if the server returns 304
            return UPDATE_OK_NO_DATA, None
        else:
            # Error happened while fetching the feed.
            self._last_timestamp = None
            return UPDATE_ERROR, None

    def _fetch_url(self) -> str | None:
        """Return URL to fetch QuakeML data from."""
        return self._url

    async def _fetch(
        self, method: str = "GET", headers=None, params=None
    ) -> tuple[str, EventParameters | None]:
        """Fetch QuakeML data from external source."""
        url = self._fetch_url()
        try:
            timeout = aiohttp.ClientTimeout(total=self._client_session_timeout())
            async with self._websession.request(
                method, url, headers=headers, params=params, timeout=timeout
            ) as response:
                try:
                    response.raise_for_status()
                    text = await self._read_response(response)
                    if text:
                        parser = XmlParser(self._additional_namespaces())
                        feed_data = parser.parse(text)
                        self.parser = parser
                        self.feed_data = feed_data
                        return UPDATE_OK, feed_data
                    else:
                        return UPDATE_OK_NO_DATA, None
                except client_exceptions.ClientError as client_error:
                    _LOGGER.warning(
                        "Fetching data from %s failed with %s", url, client_error
                    )
                    return UPDATE_ERROR, None
                except ExpatError as expat_error:
                    _LOGGER.warning(
                        "Parsing data from %s failed with %s", url, expat_error
                    )
                    return UPDATE_OK_NO_DATA, None
        except client_exceptions.ClientError as client_error:
            _LOGGER.warning(
                "Requesting data from %s failed with " "client error: %s",
                url,
                client_error,
            )
            return UPDATE_ERROR, None
        except asyncio.TimeoutError:
            _LOGGER.warning("Requesting data from %s failed with " "timeout error", url)
            return UPDATE_ERROR, None

    async def _read_response(self, response):
        """Pre-process the response."""
        if response:
            raw_response = await response.read()
            _LOGGER.debug("Response encoding %s", response.get_encoding())
            if raw_response.startswith(codecs.BOM_UTF8):
                return await response.text("utf-8-sig")
            return await response.text()
        return None

    def _filter_entries(self, entries: list[T_FEED_ENTRY]) -> list[T_FEED_ENTRY]:
        """Filter the provided entries."""
        filtered_entries: list[T_FEED_ENTRY] = entries
        _LOGGER.debug("Entries before filtering %s", filtered_entries)
        # Always remove entries without geometry.
        filtered_entries = list(
            filter(
                lambda entry: entry.coordinates is not None,
                filtered_entries,
            )
        )
        # Filter by distance.
        if self._filter_radius:
            filtered_entries = list(
                filter(
                    lambda entry: entry.distance_to_home <= self._filter_radius,
                    filtered_entries,
                )
            )
        # # Filter by category.
        if self._filter_minimum_magnitude:
            # Return only entries that have an actual magnitude value, and
            # the value is equal or above the defined threshold.
            filtered_entries = list(
                filter(
                    lambda entry: entry.magnitude
                    and entry.magnitude.mag
                    and entry.magnitude.mag >= self._filter_minimum_magnitude,
                    filtered_entries,
                )
            )
        _LOGGER.debug("Entries after filtering %s", filtered_entries)
        return filtered_entries

    def _extract_from_feed(self, feed: EventParameters) -> dict | None:
        """Extract global metadata from feed."""
        return None

    def _extract_last_timestamp(
        self, feed_entries: list[T_FEED_ENTRY]
    ) -> datetime | None:
        """Determine latest (newest) entry from the filtered feed."""
        if feed_entries:
            dates: list[datetime] = sorted(
                [
                    entry.creation_info.creation_time
                    for entry in feed_entries
                    if entry.creation_info and entry.creation_info.creation_time
                ],
                reverse=True,
            )
            if dates:
                last_timestamp: datetime = dates[0]
                _LOGGER.debug("Last timestamp: %s", last_timestamp)
                return last_timestamp
        return None

    @property
    def last_timestamp(self) -> datetime | None:
        """Return the last timestamp extracted from this feed."""
        return self._last_timestamp
