# Changes

## 0.8 (30/08/2024)
* Changed depth from integer to float (thanks @FoxxMD).
* Removed Python 3.8 support.
* Code quality improvements.

## 0.7 (02/02/2024)
* Added Python 3.12 support.
* Bumped dateparser to 1.2.0.
* Bumped haversine to 2.8.1.
* Bumped library versions: black, flake8, isort.
* Migrated to pytest.
* Code quality improvements.

## 0.6 (27/01/2023)
* Added Python 3.11 support.
* Removed deprecated asynctest dependency.
* Bumped library versions: black, dateparser, xmltodict, haversine.

## 0.5 (09/05/2022)
* Improved extensibility for implementing libraries.
* General code improvements.

## 0.4 (29/04/2022)
* Remove unnecessary print statement.
* Remove string capitalisation in two instances.

## 0.3 (29/04/2022)
* Extract last timestamp from entries' creation info.
* Fix potential bug where dynamic URL is not yet initialised.

## 0.2 (29/04/2022)
* Made feed URL dynamically configurable in case the QuakeML feed supports parameters
  that could change with each call.

## 0.1 (27/04/2022)
* Initial release as base for QuakeML feeds.
* Calculating distance to home coordinates.
* Support for filtering by distance and magnitude.
* Filter out entries without any geo location data.
* Simple Feed Manager.
