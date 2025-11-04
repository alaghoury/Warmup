"""DNS and blacklist checking utilities."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import dns.resolver

logger = logging.getLogger(__name__)

_BLACKLISTS = (
    "zen.spamhaus.org",
    "b.barracudacentral.org",
    "spam.dnsbl.sorbs.net",
)


def _lookup_mx(domain: str) -> list[str]:
    try:
        answers = dns.resolver.resolve(domain, "MX")
    except Exception as exc:  # pragma: no cover - network dependent
        logger.debug("MX lookup failed for %s: %s", domain, exc)
        return []
    records: list[str] = []
    for answer in answers:
        try:
            records.append(str(answer.exchange).rstrip("."))
        except AttributeError:
            continue
    return sorted(set(records))


def _check_blacklists(domain: str) -> list[str]:
    hits: list[str] = []
    for blacklist in _BLACKLISTS:
        query = f"{domain}.{blacklist}"
        try:
            dns.resolver.resolve(query, "A")
        except dns.resolver.NXDOMAIN:
            continue
        except Exception as exc:  # pragma: no cover - network dependent
            logger.debug("Blacklist lookup error for %s on %s: %s", domain, blacklist, exc)
            continue
        else:
            hits.append(blacklist)
    return hits


def check_domain_health(domain: str) -> dict[str, Any]:
    """Return DNS and blacklist information for a domain."""

    domain = domain.strip().lower()
    mx_records = _lookup_mx(domain)
    blacklist_hits = _check_blacklists(domain)
    warnings = []
    if not mx_records:
        warnings.append("No MX records found.")
    if blacklist_hits:
        warnings.append("Domain appears on known blacklists.")
    return {
        "domain": domain,
        "mx_records": mx_records,
        "blacklist_hits": blacklist_hits,
        "warnings": warnings,
        "checked_at": datetime.utcnow(),
    }


__all__ = ["check_domain_health"]
