# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---
Here is the changelog for version 0.1.2 based on the modifications we discussed for `GeomaterialRetriever` and `LocalitiesRetriever`.

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
