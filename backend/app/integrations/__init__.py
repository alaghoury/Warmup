"""Email provider integration helpers."""
from __future__ import annotations

from typing import Callable, Mapping

from . import gmail_integration, outlook_integration, smtp_integration

ConnectorFunc = Mapping[str, Callable]

_PROVIDERS: dict[str, ConnectorFunc] = {
    "gmail": gmail_integration.CONNECTOR,
    "google": gmail_integration.CONNECTOR,
    "outlook": outlook_integration.CONNECTOR,
    "microsoft": outlook_integration.CONNECTOR,
    "smtp": smtp_integration.CONNECTOR,
    "imap": smtp_integration.CONNECTOR,
    "generic": smtp_integration.CONNECTOR,
}


def get_connector(provider: str) -> ConnectorFunc:
    """Return an integration connector for the given provider key.

    Parameters
    ----------
    provider:
        Provider slug supplied by the API consumer (case-insensitive).

    Raises
    ------
    KeyError
        If no connector exists for the requested provider.
    """

    key = provider.lower()
    if key not in _PROVIDERS:
        raise KeyError(f"Unsupported provider '{provider}'.")
    return _PROVIDERS[key]


__all__ = ["get_connector"]
