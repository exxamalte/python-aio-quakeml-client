"""Tests for QuakeML library."""
from typing import Dict, Optional, Tuple

from aio_quakeml_client.feed import QuakeMLFeed
from aio_quakeml_client.feed_entry import FeedEntry
from aio_quakeml_client.xml_parser.event import Event


class MockFeedEntry(FeedEntry):
    """Mock feed entry."""

    @property
    def attribution(self) -> Optional[str]:
        """No attribution in mock feed entry."""
        return None


class MockQuakeMLFeed(QuakeMLFeed[MockFeedEntry]):
    """Mock feed producing mock feed entries."""

    def _new_entry(
        self, home_coordinates: Tuple[float, float], event: Event, global_data: Dict
    ) -> MockFeedEntry:
        """Generate a new mock feed entry."""
        return MockFeedEntry(home_coordinates, event)


class MockConfigurabelUrlQuakeMLFeed(MockQuakeMLFeed):
    """Mock feed with custom URL."""

    def _fetch_url(self):
        """Return URL to fetch QuakeML data from."""
        return "http://test.url/customtestpath"
