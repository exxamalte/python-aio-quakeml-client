"""Tests for QuakeML library."""
from typing import Dict, Optional, Tuple

from aio_quakeml_client.feed import QuakeMLFeed
from aio_quakeml_client.feed_entry import FeedEntry
from aio_quakeml_client.xml_parser.event import Event


class MockFeedEntry(FeedEntry):
    @property
    def attribution(self) -> Optional[str]:
        return None


class MockQuakeMLFeed(QuakeMLFeed[MockFeedEntry]):
    def _extract_from_feed(self, feed) -> Optional:
        return None

    def _new_entry(
        self, home_coordinates: Tuple[float, float], event: Event, global_data: Dict
    ) -> MockFeedEntry:
        return MockFeedEntry(home_coordinates, event)


class MockConfigurabelUrlQuakeMLFeed(MockQuakeMLFeed):
    def _fetch_url(self):
        """Return URL to fetch QuakeML data from."""
        return "http://test.url/customtestpath"
