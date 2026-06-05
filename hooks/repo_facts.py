"""MkDocs hook: fetch per-project GitHub stars/forks at build time.

The header shows a per-project repository link (see
``overrides/partials/source.html``). Material's built-in "repository facts" are
fetched client-side and cached under a single global key, which is unreliable on
a multi-repo site — whichever repo loads first wins for the whole session. So
instead we fetch the star/fork counts here, at build time, and render them
statically into the header. This is deterministic, verifiable in the built HTML,
and makes zero API calls from visitors' browsers.

Results are cached locally (1 hour TTL) so ``mkdocs serve`` auto-reloads and
repeated local builds don't exhaust GitHub's unauthenticated rate limit. Any
network/API failure is non-fatal: the facts are simply omitted and the header
still shows the repository link.
"""

from __future__ import annotations

import json
import logging
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger("mkdocs.hooks.repo_facts")

# Map the per-page repo slug (see source.html branching) to a GitHub repo.
REPOS: Dict[str, str] = {
    "deeplens": "vccimaging/DeepLens",
    "end2end": "vccimaging/End2endImaging",
    "difftmm": "AI4Optics/DiffTMM",
}

_CACHE_FILE = Path(".cache/repo_facts.json")
_CACHE_TTL = 3600  # seconds


def _format_count(n: int) -> str:
    """Compact number format matching Material's ``br()`` (e.g. 642, 1.2k)."""
    if n > 999:
        decimals = 1 if (n - 950) % 1000 > 99 else 0
        return f"{(n + 1e-6) / 1000:.{decimals}f}k"
    return str(n)


def _fetch_repo(full_name: str) -> Optional[Dict[str, str]]:
    url = f"https://api.github.com/repos/{full_name}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "AI4Optics-docs",
            "Accept": "application/vnd.github+json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.load(resp)
        return {
            "stars": _format_count(int(data["stargazers_count"])),
            "forks": _format_count(int(data["forks_count"])),
        }
    except Exception as exc:  # network, HTTP, JSON, rate-limit — all non-fatal
        logger.warning("repo_facts: could not fetch %s (%s)", full_name, exc)
        return None


def _load_cache() -> Optional[Dict[str, Any]]:
    try:
        blob = json.loads(_CACHE_FILE.read_text())
        if time.time() - blob.get("fetched_at", 0) < _CACHE_TTL:
            return blob.get("facts")
    except Exception:
        pass
    return None


def _save_cache(facts: Dict[str, Any]) -> None:
    try:
        _CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        _CACHE_FILE.write_text(
            json.dumps({"fetched_at": time.time(), "facts": facts})
        )
    except Exception:
        pass


def on_config(config, **kwargs):
    facts = _load_cache()
    if facts is None:
        facts = {slug: _fetch_repo(name) for slug, name in REPOS.items()}
        # Only cache when at least one fetch succeeded, so a transient offline
        # build doesn't pin an all-empty result for the next hour.
        if any(facts.values()):
            _save_cache(facts)
    extra = config.get("extra") or {}
    extra["repo_facts"] = facts
    config["extra"] = extra
    logger.info("repo_facts: %s", {k: bool(v) for k, v in facts.items()})
    return config
