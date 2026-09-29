"""Exceptions raised by openmindat.

Every error subclasses ``ValueError`` as well as ``MindatError``, because
openmindat <= 0.1.3 raised plain ``ValueError`` for API failures. Existing
``except ValueError:`` handlers keep working; new code can catch ``MindatError``.
"""

from __future__ import annotations

from typing import Any


class MindatError(Exception):
    """Base class for all openmindat errors."""


class MindatApiError(MindatError, ValueError):
    """The Mindat API answered with an error or could not be used.

    ``partial_results`` holds any records already downloaded before the failure.
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        url: str | None = None,
        payload: Any = None,
        partial_results: list[Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.url = url
        self.payload = payload
        self.partial_results = partial_results if partial_results is not None else []


class MindatServerError(MindatApiError):
    """The Mindat API server failed (5xx, gateway timeout, rate limit, network).

    This is a problem on the Mindat server side, not in openmindat.
    """


class MindatRequestError(MindatApiError):
    """The Mindat API rejected the request (HTTP 4xx), e.g. an unknown id or a bad parameter."""


class EndpointUnavailableError(MindatApiError):
    """The wrapped endpoint no longer exists in the Mindat API."""

    def __init__(self, message: str, endpoint: str) -> None:
        super().__init__(message, status_code=404)
        self.endpoint = endpoint


class MindatApiKeyError(MindatError, ValueError):
    """No usable Mindat API key could be found or entered."""


class MindatApiKeyNotFoundError(MindatApiKeyError, FileNotFoundError):
    """No stored Mindat API key exists.

    Also a ``FileNotFoundError``, which is what openmindat <= 0.1.3 raised from
    ``MindatApiKeyManager.load_api_key()`` when no key file existed.
    """


class MindatApiKeyPromptError(MindatApiKeyError, EOFError):
    """No stored key was found and nobody could answer the key prompt (no input available).

    Also an ``EOFError``, which is what openmindat <= 0.1.3 raised in that situation.
    """


class MindatKeyWarning(UserWarning):
    """A stored Mindat API key was rejected, unreadable, or could not be verified."""
