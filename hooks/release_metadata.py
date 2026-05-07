from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


LATEST_RELEASE_API_URL = "https://api.github.com/repos/un-nf/404/releases/latest"
FALLBACK_RELEASE_TAG = "the latest GitHub release"
FALLBACK_RELEASE_URL = "https://github.com/un-nf/404/releases/latest"

_release_tag = FALLBACK_RELEASE_TAG
_release_url = FALLBACK_RELEASE_URL


def _fetch_latest_release() -> tuple[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "404-docs-mkdocs-build",
    }

    github_token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    request = urllib.request.Request(LATEST_RELEASE_API_URL, headers=headers)

    with urllib.request.urlopen(request, timeout=10) as response:
        payload = json.load(response)

    release_tag = str(payload.get("tag_name") or "").strip() or FALLBACK_RELEASE_TAG
    release_url = str(payload.get("html_url") or "").strip() or FALLBACK_RELEASE_URL
    return release_tag, release_url


def on_config(config, **kwargs):
    global _release_tag, _release_url

    try:
        _release_tag, _release_url = _fetch_latest_release()
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError):
        _release_tag = FALLBACK_RELEASE_TAG
        _release_url = FALLBACK_RELEASE_URL

    return config


def on_page_markdown(markdown, **kwargs):
    return (
        markdown.replace("{{ latest_github_release_tag }}", _release_tag)
        .replace("{{ latest_github_release_url }}", _release_url)
    )