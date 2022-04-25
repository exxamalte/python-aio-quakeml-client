"""aio_quakeml_client library."""
from typing import Dict, Optional, Tuple

from aio_quakeml_client.feed import T_FEED_ENTRY, QuakeMLFeed
from aio_quakeml_client.feed_entry import FeedEntry
from aio_quakeml_client.xml_parser.event import Event


class TestFeedEntry(FeedEntry):
    @property
    def attribution(self) -> Optional[str]:
        return None


class TestFeed(QuakeMLFeed):
    def _new_entry(
        self, home_coordinates: Tuple[float, float], rss_entry: Event, global_data: Dict
    ) -> T_FEED_ENTRY:
        return TestFeedEntry(home_coordinates, rss_entry)
