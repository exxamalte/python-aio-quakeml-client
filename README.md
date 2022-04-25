# python-aio-quakeml-client

[![Build Status](https://github.com/exxamalte/python-aio-quakeml-client/workflows/CI/badge.svg?branch=main)](https://github.com/exxamalte/python-aio-quakeml-client/actions?workflow=CI)
[![codecov](https://codecov.io/gh/exxamalte/python-aio-quakeml-client/branch/main/graph/badge.svg?token=97PBJ93VGE)](https://codecov.io/gh/exxamalte/python-aio-quakeml-client)
[![PyPi](https://img.shields.io/pypi/v/aio-quakeml-client.svg)](https://pypi.python.org/pypi/aio-quakeml-client)
[![Version](https://img.shields.io/pypi/pyversions/aio-quakeml-client.svg)](https://pypi.python.org/pypi/aio-quakeml-client)

This library provides convenient async access to QuakeML feeds.


**Example**
```python
import asyncio
from aiohttp import ClientSession
from aio_quakeml_client import TestFeed
async def main() -> None:
    async with ClientSession() as websession:    
        # Home Coordinates: Latitude: -33.0, Longitude: 150.0
        # Filter radius: 500 km
        feed = TestFeed(websession, 
                        (-33.0, 150.0),
                        url="https://webservices.ingv.it/fdsnws/event/1/query?starttime=2022-03-01T00:00:00&endtime=2022-03-01T23:59:59",
                        filter_radius=50000)
        status, entries = await feed.update()
        print(status)
        print(entries)
asyncio.get_event_loop().run_until_complete(main())
```
