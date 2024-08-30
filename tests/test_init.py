"""Tests for QuakeML feed general setup."""

from aio_quakeml_client import __version__


def test_version():
    """Test for version tag."""
    assert __version__ is not None
