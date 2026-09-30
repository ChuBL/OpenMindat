# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.1.4] - 2026-09-30

Backward compatible with 0.1.3: existing code keeps working. The behaviour changes that users may notice are listed under "Changed".

### Added

- **LocalityTranslationsRetriever** and **LocalityTranslationsIdRetriever** for the new `/locality-translations/` endpoint, with `lt_loc()`, `lt_iso()`, `lt_text()`, `lt_important()`, `lt_datetime_gte()`, `ordering()` and `page()`.
- **GeomaterialDictRetriever**: `field()`. The API requires it, e.g. `field("csystem")`.
- **GeomaterialSearchRetriever**: `e()` (exact matches only), `ima()` (IMA-approved only) and `size()`.
- **LocalitiesRetriever**: `level_gte()`, `level_lte()`, `sublocs_gte()`, `sublocs_lte()`, `revtxtd_istartswith()` and `non_hierarchial()`. The last one is spelled as in the Mindat API; `non_hierarchical()` is an alias.
- **LocalitiesIdRetriever**: `country()`.
- **MineralsIMARetriever**: the 36 geomaterial filters the endpoint supports, such as `crystal_system()`, `hardness_min()`, `el_inc()` and `ima_status()`, plus the aliases `color()`, `diaphaneity()`, `elements_inc()` and `elements_exc()`.
- Exceptions, all importable from `openmindat`: `MindatError`, `MindatApiError`, `MindatServerError`, `MindatRequestError`, `EndpointUnavailableError` and `MindatApiKeyError`. Each one is also a `ValueError`, so existing `except ValueError:` code keeps working.
- `openmindat.set_api_key(key, persist=False)` and `openmindat.api_key_status()`.
- Settings on `MindatApi`: `REQUEST_TIMEOUT`, `RAISE_HTTP_ERRORS`, `MIN_PAGE_SIZE`, `MAX_RETRY_WAIT` and `MAX_FAILURES`.
- Type hints on all public methods. IDE completion now works along chained calls.

### Changed

- **HTTP errors now raise an exception instead of returning the error as data.**
  - A 4xx response used to come back as `{"results": [{"detail": ...}]}`. It now raises `MindatRequestError` with the server's message.
  - 5xx responses, gateway timeouts, rate limits and network failures raise `MindatServerError`. Its message says the problem is on the Mindat server side.
  - To restore the old behaviour, set `openmindat.MindatApi.RAISE_HTTP_ERRORS = False`.
- **Heavy queries recover automatically.**
  - Requests now have a timeout (10 s to connect, 60 s to read); previously there was none.
  - A page that times out (HTTP 504/524 or a read timeout) is requested again as smaller pages.
  - Rate limits (HTTP 429/503) wait for the server's `Retry-After`, capped at 30 s.
  - Retries are limited, and records downloaded before a failure are kept on the exception as `.partial_results`.
- **API key handling.**
  - The key is checked once per session instead of before every query, so each query sends one request instead of two.
  - A key typed at the prompt is saved to `~/.config/openmindat/credentials.yaml` (`%APPDATA%\openmindat\credentials.yaml` on Windows), readable only by you, instead of `./.apikey.yaml` in the current folder.
  - An existing `./.apikey.yaml` is still read, and is copied once to the new location. The old file is left in place.
  - A key set through `MINDAT_API_KEY` is no longer written to disk.
  - A temporary server problem during the key check no longer triggers the key prompt. The key is used, and a warning is shown.
  - With no key and no console (scripts, cron, CI), you now get `MindatApiKeyError` with setup instructions instead of a bare `EOFError`. The new error is still an `EOFError`, so existing handlers keep working.
- `DanaRetriever` and `StrunzRetriever` used without `.groups()`, `.classes()` or similar now say which method to call. The Mindat API has no plain list for these endpoints.
- Retry messages go to the `openmindat` logger, and are also printed when `verbose` is above 0.

### Deprecated

- `CountriesListRetriever`, `CountriesIdRetriever`, `GeoRegionRetriever`, `LocobjectRetriever` and `PhotoCountRetriever` (in `openmindat._countries`, `._locgeoregion2`, `._locobject` and `._photo_count`). Their Mindat endpoints no longer exist.
  - They can still be imported. Creating one shows a `DeprecationWarning`.
  - Querying one raises `EndpointUnavailableError`, a `ValueError`, without sending a request.
  - They will be removed in 0.2.0.

### Fixed

- `LocalitiesRetriever.expand("geomaterials")` with a string split the value into letters (`g,e,o,…`), so no geomaterials were returned. A string now works like a one-item list.
- `GeomaterialIdRetriever.varieties(True).get_dict()` now requests `/geomaterials/{id}/varieties/`, as `saveto()` already did.
- The first query of a `GeomaterialSearchRetriever` now sends the same default parameters as later ones. A failed first query no longer raises `KeyError`.
- A page requested with `.page(n)` could return the wrong records when the server timed out and the page size was reduced. The requested page is now returned in full.
- A failure part-way through a multi-page download no longer discards the records already downloaded.
- A corrupted `./.apikey.yaml` is skipped with a warning instead of crashing with `TypeError` or `KeyError`.
- The `entrytype()` error message now lists the valid options.

### Known Issues (Mindat API server)

- `MineralsIMARetriever.fields()` fails with HTTP 500 when the field list includes `name`. This has been reported to Mindat.
- `GeomaterialDictRetriever.field()` with an unknown field name gets HTTP 200 with an error message instead of an error status, so `field()` warns about unknown names itself.
- `GeomaterialSearchRetriever.size()` currently has no visible effect on the server.

## [0.1.3] - 2026-01-29

### Added

- **GeomaterialRetriever**:
- Added `el_essential()` method to filter searches to essential elements only.
- Added `id_min()` and `id_max()` methods to support filtering by ID ranges.


- **LocalitiesRetriever**:
- Added `page()` method to support the new pagination parameter in the Localities API.



### Changed

- **GeomaterialRetriever**:
- Updated internal parameter keys to match the latest Mindat API v1 schema:
- `cleavage_type` -> `cleavagetype`
- `diaphaneity` -> `diapheny`
- `elements_exc` -> `el_exc`
- `elements_inc` -> `el_inc`
- `entry_type` -> `entrytype`
- `fracture_type` -> `fracturetype`

- Added aliases for renamed methods (`elements_exc`, `elements_inc`, `diaphaneity`) to maintain backward compatibility.


- **LocalitiesRetriever**:
- Removed strict hardcoded validation for the `country()` method to improve resilience against API data updates.
- Updated pagination logic to prioritize `page` over the legacy `cursor` parameter.


### Deprecated

- **LocalitiesRetriever**:
- The `cursor()` method is now deprecated as the Localities API has transitioned to page-based pagination.


### Known Issues

- Migration to the new API schema is ongoing; some legacy endpoints not yet implemented in v1 remain unavailable.

## [0.1.2] - 2025-06-06

### Changed

- Relax Python requirement to >=3.10

## [0.1.1] - 2025-06-06

### Changed

- Fixed a spelling error in the class name `MindatApiKeyManeger` -> `MindatApiKeyManager`.
- `MindatApi` and `MindatApiKeyManager` now support an optional `ENDPOINT` parameter to customize the API endpoint.

### Fixed

- Updated several endpoints to include the `v1/` prefix to align with recent changes on the Mindat server.
- Corrected parameter names to match the official Mindat API documentation (e.g., changed `id__in` to `id_in`).

### Removed

- Removed outdated endpoint support for:
  - `countries`
  - `locgeoregion2`
  - `locobject`
  - `photocount`

  These will be reintroduced in future versions based on the new Mindat API structure.

### Known Issues

- Many existing functions and endpoints are deprecated due to recent updates on the Mindat API server.
- For the latest available endpoints and parameters, refer to the [official Mindat API documentation](https://api.mindat.org/schema/redoc/).
- The OpenMindat package is undergoing migration to support the updated API schema. This process is ongoing and may temporarily affect feature availability.

## [0.1.0] - 2025-04-23

### Changed

- Renamed some endpoint names and parameters for consistency with the Mindat API (e.g., from underscore to hyphen).
- Revised download logic to better handle oversized page sizes. Manual control is now possible to avoid server errors.

## [0.0.9] - 2024-06-17

### Added

- Introduced a `verbose` function to control save notifications and progress display.

### Changed

- Improved logic for handling large content in downloads.

### Usage

```python
.verbose(FLAG)  # where FLAG = 0 (silent), 1 (notify), 2 (default)
```

## [0.0.8] - 2024-06-09

### Added

- Function name typo detection with valid method suggestions.

### Changed

- Retry and stabilization logic in downloads.

## [0.0.7] - 2024-04-26

### Fixed

- Locality country filter now supports country-specific queries (e.g., "UK", "USA").

## [0.0.6] - 2024-04-26

### Fixed

- Bug in country endpoint’s get function.

## [0.0.5] - 2024-04-26

### Fixed

- Internal server error from v0.0.4 resolved server-side.

### Changed

- `get` functions renamed to `get_dict`.
- Added progress bars for paged downloads.

## [0.0.4] - 2024-04-14

### Added

- Option to get list object of data directly in addition to saving locally.

### Known Issues

- Multi-page data queries may still result in internal server errors.
  See: [GitHub Issue #12](https://github.com/ChuBL/OpenMindat/issues/12)

## [0.0.3] - 2024-04-11

### Added

- More endpoint support (not fully tested).

### Changed

- Revised API key retrieval logic.

## [0.0.1] - 2023-12-14

### Added

- Initial release of the OpenMindat package.
