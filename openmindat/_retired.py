"""Retrievers for endpoints the Mindat API has removed.

Each retired retriever is generated from one row of ``RETIRED_ENDPOINTS`` so old
imports and call chains keep working: constructing one emits a
``DeprecationWarning``, chain methods return ``self``, and ``get_dict()``,
``save()`` and ``saveto()`` raise ``EndpointUnavailableError`` (a
``ValueError``) without sending a request.

Lifecycle: a retired retriever is kept for the rest of the minor release series
in which it was retired and deleted at the next minor version (``remove_in``).
To retire another endpoint, add a row here, define the class below, and reduce
its old module to a one-line import from this module.
"""

from __future__ import annotations

import warnings
from typing import Any, NoReturn

from .exceptions import EndpointUnavailableError

RETIRED_ENDPOINTS: dict[str, dict[str, Any]] = {
    "CountriesListRetriever": {
        "module": "openmindat._countries",
        "endpoint": "countries",
        "methods": ("page", "page_size", "verbose"),
        "first_seen_missing": "2026-05-27",
        "remove_in": "0.2.0",
    },
    "CountriesIdRetriever": {
        "module": "openmindat._countries",
        "endpoint": "countries/{id}",
        "methods": ("id", "page_size", "verbose"),
        "first_seen_missing": "2026-05-27",
        "remove_in": "0.2.0",
    },
    "GeoRegionRetriever": {
        "module": "openmindat._locgeoregion2",
        "endpoint": "locgeoregion2",
        "methods": ("page", "page_size", "verbose"),
        "first_seen_missing": "2026-05-27",
        "remove_in": "0.2.0",
    },
    "LocobjectRetriever": {
        "module": "openmindat._locobject",
        "endpoint": "locobject/{id}",
        "methods": ("id", "verbose"),
        "first_seen_missing": "2026-05-27",
        "remove_in": "0.2.0",
    },
    "PhotoCountRetriever": {
        "module": "openmindat._photo_count",
        "endpoint": "photocount",
        "methods": ("page_size", "verbose"),
        "first_seen_missing": "2026-05-27",
        "remove_in": "0.2.0",
    },
}


class _RetiredRetriever:
    """Stand-in for a retriever whose Mindat endpoint no longer exists."""

    ENDPOINT = ""
    REMOVE_IN = ""

    def __init__(self) -> None:
        warnings.warn(
            f"{type(self).__name__} is deprecated: the Mindat API no longer provides "
            f"'/{self.ENDPOINT}/'. It will be removed in openmindat {self.REMOVE_IN}.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.end_point = self.ENDPOINT.split("/")[0]
        self.verbose_flag = 2
        self._params: dict[str, Any] = {}

    def _chain(self, *args: Any, **kwargs: Any) -> _RetiredRetriever:
        return self

    def _unavailable(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise EndpointUnavailableError(
            f"{type(self).__name__} cannot run: the Mindat API no longer provides "
            f"'/{self.ENDPOINT}/' (it returns 404 Not Found). This class will be removed "
            f"in openmindat {self.REMOVE_IN}.",
            endpoint=self.ENDPOINT,
        )

    get_dict = _unavailable
    save = _unavailable
    saveto = _unavailable

    def available_methods(self) -> None:
        methods = [
            name
            for name in dir(self)
            if callable(getattr(self, name)) and not name.startswith("_")
        ]
        print("Available methods:", methods)


def _retired(name: str) -> type[_RetiredRetriever]:
    spec = RETIRED_ENDPOINTS[name]
    namespace: dict[str, Any] = {
        "__module__": spec["module"],
        "__doc__": (
            f"Retired: the Mindat API no longer provides '/{spec['endpoint']}/'. "
            f"Kept so existing code imports cleanly; removed in openmindat {spec['remove_in']}."
        ),
        "ENDPOINT": spec["endpoint"],
        "REMOVE_IN": spec["remove_in"],
    }
    for method in spec["methods"]:
        namespace[method] = _RetiredRetriever._chain
    return type(name, (_RetiredRetriever,), namespace)


CountriesListRetriever = _retired("CountriesListRetriever")
CountriesIdRetriever = _retired("CountriesIdRetriever")
GeoRegionRetriever = _retired("GeoRegionRetriever")
LocobjectRetriever = _retired("LocobjectRetriever")
PhotoCountRetriever = _retired("PhotoCountRetriever")
