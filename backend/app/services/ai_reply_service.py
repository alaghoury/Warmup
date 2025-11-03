"""Helpers for generating human-like replies using DeepSeek."""
from __future__ import annotations

import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)

_DEFAULT_DEEPSEEK_URL = os.getenv(
    "DEEPSEEK_API_URL",
    "https://api.deepseek.com/v1/chat/completions",
)


def _get_api_key() -> str | None:
    """Retrieve the DeepSeek API key from supported environment variables."""

    return os.getenv("DEEPSEEK_API_KEY") or os.getenv("deepseek_API_KEY")


async def generate_human_reply(
    email_body: str,
    language: str = "English",
    tone: str = "friendly",
    *,
    max_tokens: int = 220,
    temperature: float = 0.7,
) -> str:
    """Call DeepSeek to obtain a realistic reply for a warmup email.

    If the API call fails or the key is missing, the function returns a
    deterministic fallback message so the warmup pipeline can continue.
    """

    api_key = _get_api_key()
    fallback = (
        "Hi there, thanks for reaching out! I'm keeping an eye on our warmup "
        "run and will follow up with any updates."
    )
    if not api_key:
        logger.warning("DeepSeek API key missing; returning fallback reply")
        return fallback

    system_prompt = (
        "You are an email deliverability specialist composing concise, "
        "human-sounding replies. Use the requested language (%s) and tone (%s)."
        % (language, tone)
    )

    payload: dict[str, Any] = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    "Reply to the following message while sounding natural and "
                    "lightly conversational.\n\n" + email_body
                ),
            },
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(_DEFAULT_DEEPSEEK_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
    except Exception as exc:  # pragma: no cover - network failure path
        logger.warning("DeepSeek request failed: %s", exc)
        return fallback

    try:
        message = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):  # pragma: no cover - malformed payload
        logger.warning("Unexpected DeepSeek response payload: %s", data)
        return fallback

    return message or fallback


__all__ = ["generate_human_reply"]
