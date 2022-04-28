"""Test for the generic QuakeML feed."""
import asyncio
import datetime
from unittest.mock import MagicMock

import aiohttp
import pytest
from aiohttp import ClientOSError

from aio_quakeml_client.consts import UPDATE_ERROR, UPDATE_OK, UPDATE_OK_NO_DATA
from tests import MockConfigurabelUrlQuakeMLFeed, MockQuakeMLFeed
from tests.utils import load_fixture


@pytest.mark.asyncio
async def test_update_ok(aresponses, event_loop):
    """Test updating feed is ok."""
    home_coordinates = (-31.0, 151.0)
    aresponses.add(
        "test.url",
        "/testpath",
        "get",
        aresponses.Response(text=load_fixture("generic_feed_1.xml"), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:

        feed = MockQuakeMLFeed(websession, home_coordinates, "http://test.url/testpath")
        assert (
            repr(feed) == "<MockQuakeMLFeed(home=(-31.0, 151.0), "
            "url=http://test.url/testpath, radius=None, magnitude=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 1

        feed_entry = entries[0]
        assert feed_entry is not None
        assert (
            feed_entry.external_id
            == "smi:webservices.ingv.it/fdsnws/event/1/query?eventId=30116321"
        )

        assert feed_entry.description == "Region name: 4 km S Campotosto (AQ)"
        assert feed_entry.type == "Earthquake"

        assert (
            feed_entry.origin.public_id
            == "smi:webservices.ingv.it/fdsnws/event/1/query?originId=101595191"
        )
        assert feed_entry.coordinates == (42.5218, 13.3833)
        assert feed_entry.origin.latitude == 42.5218
        assert feed_entry.origin.longitude == 13.3833
        assert feed_entry.origin.type == "hypocenter"
        assert feed_entry.origin.depth == 14500
        assert feed_entry.origin.depth_type == "From location"
        assert feed_entry.origin.time == datetime.datetime(
            2022, 3, 1, 22, 53, 55, 680000, tzinfo=datetime.timezone.utc
        )
        assert feed_entry.origin.evaluation_status == "reviewed"
        assert feed_entry.origin.evaluation_mode == "manual"

        assert round(abs(feed_entry.distance_to_home - 16074.6), 1) == 0
        assert (
            repr(feed_entry)
            == "<MockFeedEntry(id=smi:webservices.ingv.it/fdsnws/event/1/query?eventId=30116321)>"
        )
        assert (
            feed_entry.magnitude.public_id
            == "smi:webservices.ingv.it/fdsnws/event/1/query?magnitudeId=108867501"
        )
        assert feed_entry.magnitude.type == "ML"
        assert feed_entry.magnitude.mag == 2.6
        assert feed_entry.magnitude.station_count == 72
        assert (
            repr(feed_entry.magnitude)
            == "<Magnitude(smi:webservices.ingv.it/fdsnws/event/1/query?magnitudeId=108867501)>"
        )

        assert feed_entry.creation_info.agency_id == "INGV"
        assert feed_entry.creation_info.author == "hew10_mole#MOD_EQASSEMBLE"
        assert feed_entry.creation_info.creation_time == datetime.datetime(
            2022, 3, 1, 22, 54, 13, tzinfo=datetime.timezone.utc
        )


@pytest.mark.asyncio
async def test_update_edge_cases(aresponses, event_loop):
    """Test updating feed is ok."""
    home_coordinates = (-31.0, 151.0)
    aresponses.add(
        "test.url",
        "/testpath",
        "get",
        aresponses.Response(text=load_fixture("generic_feed_2.xml"), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        feed = MockQuakeMLFeed(websession, home_coordinates, "http://test.url/testpath")
        assert (
            repr(feed) == "<MockQuakeMLFeed(home=(-31.0, 151.0), "
            "url=http://test.url/testpath, radius=None, magnitude=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 3

        feed_entry = entries[0]
        assert feed_entry is not None
        assert feed_entry.origin is not None
        assert (
            feed_entry.origin.public_id
            == "smi:webservices.ingv.it/fdsnws/event/1/query?originId=101595192"
        )
        assert feed_entry.coordinates == (42.5218, 13.3833)
        assert feed_entry.origin.depth is None
        assert feed_entry.origin.depth_type is None
        assert feed_entry.origin.time is None
        assert feed_entry.magnitude is None
        assert feed_entry.creation_info is None
        assert feed_entry.description is None

        feed_entry = entries[1]
        assert feed_entry is not None
        assert feed_entry.magnitude is not None
        assert feed_entry.magnitude.mag == 2.7
        assert feed_entry.creation_info is not None
        assert feed_entry.creation_info.creation_time == datetime.datetime(
            2022, 4, 28, 10, 0, 0, 0, tzinfo=datetime.timezone.utc
        )

        assert feed.last_timestamp == datetime.datetime(
            2022, 4, 28, 11, 0, 0, 0, tzinfo=datetime.timezone.utc
        )


@pytest.mark.asyncio
async def test_update_ok_with_radius_filter(aresponses, event_loop):
    """Test updating feed is ok."""
    home_coordinates = (42.0, 13.0)
    aresponses.add(
        "test.url",
        "/testpath",
        "get",
        aresponses.Response(text=load_fixture("generic_feed_3.xml"), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        feed = MockQuakeMLFeed(
            websession,
            home_coordinates,
            "http://test.url/testpath",
            filter_radius=250.0,
        )
        assert (
            repr(feed) == "<MockQuakeMLFeed(home=(42.0, 13.0), "
            "url=http://test.url/testpath, radius=250.0, magnitude=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 2

        assert round(abs(entries[0].distance_to_home - 66.0), 1) == 0
        assert round(abs(entries[1].distance_to_home - 203.4), 1) == 0


@pytest.mark.asyncio
async def test_update_ok_with_magnitude_filter(aresponses, event_loop):
    """Test updating feed is ok."""
    home_coordinates = (42.0, 13.0)
    aresponses.add(
        "test.url",
        "/testpath",
        "get",
        aresponses.Response(text=load_fixture("generic_feed_3.xml"), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        feed = MockQuakeMLFeed(
            websession,
            home_coordinates,
            "http://test.url/testpath",
            filter_minimum_magnitude=3.0,
        )
        assert (
            repr(feed) == "<MockQuakeMLFeed(home=(42.0, 13.0), "
            "url=http://test.url/testpath, radius=None, magnitude=3.0)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 2

        assert entries[0].magnitude.mag == 3.6
        assert entries[1].magnitude.mag == 4.6


@pytest.mark.asyncio
async def test_update_with_configurable_url(aresponses, event_loop):
    """Test updating feed is ok."""
    home_coordinates = (-31.0, 151.0)
    aresponses.add(
        "test.url",
        "/customtestpath",
        "get",
        aresponses.Response(text=load_fixture("generic_feed_1.xml"), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:

        feed = MockConfigurabelUrlQuakeMLFeed(websession, home_coordinates)
        assert (
            repr(feed) == "<MockConfigurabelUrlQuakeMLFeed(home=(-31.0, 151.0), "
            "url=http://test.url/customtestpath, radius=None, magnitude=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 1

        feed_entry = entries[0]
        assert feed_entry is not None
        assert (
            feed_entry.external_id
            == "smi:webservices.ingv.it/fdsnws/event/1/query?eventId=30116321"
        )


@pytest.mark.asyncio
async def test_update_with_client_exception(event_loop):
    """Test updating feed results in error."""
    home_coordinates = (-31.0, 151.0)

    async with aiohttp.ClientSession(loop=event_loop):
        mock_websession = MagicMock()
        mock_websession.request.side_effect = ClientOSError
        feed = MockQuakeMLFeed(
            mock_websession, home_coordinates, "http://test.url/badpath"
        )
        status, entries = await feed.update()
        assert status == UPDATE_ERROR
        assert feed.last_timestamp is None


@pytest.mark.asyncio
async def test_update_with_timeout_error(event_loop):
    """Test updating feed results in timeout error."""
    home_coordinates = (-31.0, 151.0)

    async with aiohttp.ClientSession(loop=event_loop):
        mock_websession = MagicMock()
        mock_websession.request.side_effect = asyncio.TimeoutError
        feed = MockQuakeMLFeed(
            mock_websession, home_coordinates, "http://test.url/goodpath"
        )
        status, entries = await feed.update()
        assert status == UPDATE_ERROR
        assert feed.last_timestamp is None


@pytest.mark.asyncio
async def test_update_with_request_exception(aresponses, event_loop):
    """Test updating feed results in error."""
    home_coordinates = (-31.0, 151.0)
    aresponses.add("test.url", "/badpath", "get", aresponses.Response(status=404))

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        feed = MockQuakeMLFeed(websession, home_coordinates, "http://test.url/badpath")
        status, entries = await feed.update()
        assert status == UPDATE_ERROR
        assert feed.last_timestamp is None


@pytest.mark.asyncio
async def test_update_with_xml_decode_error(aresponses, event_loop):
    """Test updating feed raises exception."""
    home_coordinates = (-31.0, 151.0)
    aresponses.add(
        "test.url", "/badxml", "get", aresponses.Response(text="NOT XML", status=200)
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        feed = MockQuakeMLFeed(websession, home_coordinates, "http://test.url/badjson")
        status, entries = await feed.update()
        assert status == UPDATE_ERROR
        assert entries is None


@pytest.mark.asyncio
async def test_update_bom(aresponses, event_loop):
    """Test updating feed with BOM (byte order mark) is ok."""
    home_coordinates = (-31.0, 151.0)
    xml = (
        "\xef\xbb\xbf<?xml version='1.0' encoding='utf-8'?>"
        '<q:quakeml xmlns:q="http://quakeml.org/xmlns/quakeml/1.2"><eventParameters '
        'publicID="smi:webservices.ingv.it/fdsnws/event/1/query"><event><origin '
        'publicID="smi:webservices.ingv.it/fdsnws/event/1/query?originId=101595192">'
        "<latitude><value>42.5218</value></latitude><longitude><value>42.5218</value>"
        "</longitude></origin></event></eventParameters></q:quakeml>"
    )
    aresponses.add(
        "test.url",
        "/testpath",
        "get",
        aresponses.Response(text=xml, charset="iso-8859-1", status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        feed = MockQuakeMLFeed(websession, home_coordinates, "http://test.url/testpath")
        assert (
            repr(feed) == "<MockQuakeMLFeed(home=(-31.0, 151.0), "
            "url=http://test.url/testpath, radius=None, "
            "magnitude=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 1


@pytest.mark.asyncio
async def test_update_not_xml(aresponses, event_loop):
    """Test updating feed where returned payload is not XML."""
    # If a server returns invalid payload (00 control characters) this results in an
    # exception thrown: ExpatError: not well-formed (invalid token): line 1, column 0
    home_coordinates = (-31.0, 151.0)
    not_xml = "\x00\x00\x00"
    aresponses.add(
        "test.url",
        "/testpath",
        "get",
        aresponses.Response(text=not_xml, status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        feed = MockQuakeMLFeed(websession, home_coordinates, "http://test.url/testpath")
        assert (
            repr(feed) == "<MockQuakeMLFeed(home=(-31.0, 151.0), "
            "url=http://test.url/testpath, radius=None, "
            "magnitude=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK_NO_DATA
        assert entries is None
