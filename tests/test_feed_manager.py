"""Test for the generic QuakeML feed manager."""
import asyncio
from http import HTTPStatus

import aiohttp
import pytest

from aio_quakeml_client.feed_manager import QuakeMLFeedManagerBase
from tests import MockQuakeMLFeed
from tests.utils import load_fixture


@pytest.mark.asyncio
async def test_feed_manager(mock_aioresponse):
    """Test the feed manager."""
    home_coordinates = (-31.0, 151.0)
    mock_aioresponse.get(
        "http://test.url/testpath",
        status=HTTPStatus.OK,
        body=load_fixture("generic_feed_3.xml"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = MockQuakeMLFeed(websession, home_coordinates, "http://test.url/testpath")

        # This will just record calls and keep track of external ids.
        generated_entity_external_ids = []
        updated_entity_external_ids = []
        removed_entity_external_ids = []

        async def _generate_entity(external_id):
            """Generate new entity."""
            generated_entity_external_ids.append(external_id)

        async def _update_entity(external_id):
            """Update entity."""
            updated_entity_external_ids.append(external_id)

        async def _remove_entity(external_id):
            """Remove entity."""
            removed_entity_external_ids.append(external_id)

        feed_manager = QuakeMLFeedManagerBase(
            feed, _generate_entity, _update_entity, _remove_entity
        )
        assert (
            repr(feed_manager) == "<QuakeMLFeedManagerBase(feed=<"
            "MockQuakeMLFeed(home=(-31.0, 151.0), "
            "url=http://test.url/testpath, "
            "radius=None, magnitude=None)>)>"
        )
        await feed_manager.update()
        entries = feed_manager.feed_entries
        assert entries is not None
        assert len(entries) == 3
        assert feed_manager.last_update is not None
        assert feed_manager.last_timestamp is None

        assert len(generated_entity_external_ids) == 3
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 0

        feed_entry = entries.get("11")
        assert feed_entry.external_id == "11"
        assert feed_entry.description == "Description 11"
        assert feed_entry.coordinates == (42.5218, 13.3833)
        assert round(abs(feed_entry.distance_to_home - 16074.6), 1) == 0
        assert feed_entry.magnitude.mag == 2.6
        assert repr(feed_entry) == "<MockFeedEntry(id=11)>"

        feed_entry = entries.get("21")
        assert feed_entry.external_id == "21"
        assert feed_entry.magnitude.mag == 3.6

        feed_entry = entries.get("31")
        assert feed_entry.external_id == "31"
        assert feed_entry.magnitude.mag == 4.6

        # Simulate an update with several changes.
        generated_entity_external_ids.clear()
        updated_entity_external_ids.clear()
        removed_entity_external_ids.clear()

        mock_aioresponse.get(
            "http://test.url/testpath",
            status=HTTPStatus.OK,
            body=load_fixture("generic_feed_4.xml"),
        )

        await feed_manager.update()
        entries = feed_manager.feed_entries
        assert entries is not None
        assert len(entries) == 3
        assert len(generated_entity_external_ids) == 1
        assert len(updated_entity_external_ids) == 2
        assert len(removed_entity_external_ids) == 1

        feed_entry = entries.get("11")
        assert feed_entry.description == "Description 11 UPDATED"
        assert feed_entry.magnitude.mag == 2.6

        feed_entry = entries.get("21")
        assert feed_entry.magnitude.mag == 3.7

        feed_entry = entries.get("41")
        assert feed_entry.magnitude.mag == 5.6

        # Simulate an update with no data.
        generated_entity_external_ids.clear()
        updated_entity_external_ids.clear()
        removed_entity_external_ids.clear()

        mock_aioresponse.get(
            "http://test.url/testpath",
            status=HTTPStatus.OK,
        )

        await feed_manager.update()
        entries = feed_manager.feed_entries

        assert len(entries) == 3
        assert len(generated_entity_external_ids) == 0
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 0

        # Simulate an update producing an error.
        generated_entity_external_ids.clear()
        updated_entity_external_ids.clear()
        removed_entity_external_ids.clear()

        mock_aioresponse.get(
            "http://test.url/testpath",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

        await feed_manager.update()
        entries = feed_manager.feed_entries

        assert len(entries) == 0
        assert len(generated_entity_external_ids) == 0
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 3

        # Simulate an update with dynamic filter.
        generated_entity_external_ids.clear()
        updated_entity_external_ids.clear()
        removed_entity_external_ids.clear()


@pytest.mark.asyncio
async def test_feed_manager_with_status_callback(mock_aioresponse):
    """Test the feed manager."""
    home_coordinates = (-31.0, 151.0)
    mock_aioresponse.get(
        "http://test.url/testpath",
        status=HTTPStatus.OK,
        body=load_fixture("generic_feed_3.xml"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = MockQuakeMLFeed(websession, home_coordinates, "http://test.url/testpath")

        # This will just record calls and keep track of external ids.
        generated_entity_external_ids = []
        updated_entity_external_ids = []
        removed_entity_external_ids = []
        status_update = []

        async def _generate_entity(external_id):
            """Generate new entity."""
            generated_entity_external_ids.append(external_id)

        async def _update_entity(external_id):
            """Update entity."""
            updated_entity_external_ids.append(external_id)

        async def _remove_entity(external_id):
            """Remove entity."""
            removed_entity_external_ids.append(external_id)

        async def _status(status_details):
            """Capture status update details."""
            status_update.append(status_details)

        feed_manager = QuakeMLFeedManagerBase(
            feed, _generate_entity, _update_entity, _remove_entity, _status
        )
        assert (
            repr(feed_manager) == "<QuakeMLFeedManagerBase(feed=<"
            "MockQuakeMLFeed(home=(-31.0, 151.0), "
            "url=http://test.url/testpath, "
            "radius=None, magnitude=None)>)>"
        )
        await feed_manager.update()
        entries = feed_manager.feed_entries
        assert entries is not None
        assert len(entries) == 3
        assert feed_manager.last_update is not None
        assert feed_manager.last_timestamp is None

        assert len(generated_entity_external_ids) == 3
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 0

        assert status_update[0].status == "OK"
        assert status_update[0].last_update is not None
        last_update_successful = status_update[0].last_update_successful
        assert status_update[0].last_update == last_update_successful
        assert status_update[0].last_timestamp is None
        assert status_update[0].total == 3
        assert status_update[0].created == 3
        assert status_update[0].updated == 0
        assert status_update[0].removed == 0
        assert (
            repr(status_update[0]) == f"<StatusUpdate("
            f"OK@{status_update[0].last_update})>"
        )

        # Simulate an update with no data.
        generated_entity_external_ids.clear()
        updated_entity_external_ids.clear()
        removed_entity_external_ids.clear()
        status_update.clear()

        mock_aioresponse.get(
            "http://test.url/testpath",
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

        await feed_manager.update()
        entries = feed_manager.feed_entries

        assert len(entries) == 0
        assert len(generated_entity_external_ids) == 0
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 3

        assert status_update[0].status == "ERROR"
        assert status_update[0].last_update is not None
        assert status_update[0].last_update_successful is not None
        assert status_update[0].last_update_successful == last_update_successful
        assert status_update[0].total == 0
