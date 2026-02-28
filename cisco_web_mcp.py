from __future__ import annotations

import re
from http.cookies import SimpleCookie
from dataclasses import dataclass
from urllib.parse import urlparse

from fastmcp import FastMCP
from playwright._impl._api_structures import SetCookieParam
from playwright.sync_api import sync_playwright

mcp = FastMCP("Cisco Web (Playwright, Read-Only)")

ALLOWED_HOST_REGEX = r"(^|\.)cisco\.com$"

MAX_CHARS = 200000
NAV_TIMEOUT_MS = 15000
WAIT_MS = 1000

COOKIE_HEADER = ""


@dataclass
class WebPageResult:
    url: str
    title: str
    text: str


def _host_allowed(url: str) -> str:
    u = urlparse(url)
    if u.scheme not in ("https", "http"):
        raise ValueError("Only http/https URLs allowed")

    host = (u.hostname or "").lower()
    if not host:
        raise ValueError("URL missing hostname")

    if not re.search(ALLOWED_HOST_REGEX, host):
        raise ValueError(f"Host not allowed: {host}")

    return host


def _cookie_header_to_list(
    cookie_header: str, url: str
) -> list[SetCookieParam]:
    cookies: list[SetCookieParam] = []
    if not cookie_header:
        return cookies

    parsed = urlparse(url)
    cookie_url = f"{parsed.scheme}://{parsed.netloc}"

    jar = SimpleCookie()
    jar.load(cookie_header)

    for morsel in jar.values():
        if not morsel.key:
            continue

        cookies.append(
            {
                "name": morsel.key,
                "value": morsel.value,
                "url": cookie_url,
            }
        )

    return cookies


def _trim_text(text: str) -> str:
    if len(text) <= MAX_CHARS:
        return text
    return text[:MAX_CHARS] + "\n[TRUNCATED]"


@mcp.tool
def cisco_fetch(url: str) -> WebPageResult:
    _host_allowed(url)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        cookies = _cookie_header_to_list(COOKIE_HEADER, url=url)
        if cookies:
            context.add_cookies(cookies)

        page = context.new_page()
        page.set_default_navigation_timeout(NAV_TIMEOUT_MS)
        page.set_default_timeout(NAV_TIMEOUT_MS)

        page.goto(url, wait_until="domcontentloaded")
        if WAIT_MS > 0:
            page.wait_for_timeout(WAIT_MS)

        title = page.title() or ""
        text = page.inner_text("body")

        context.close()
        browser.close()

    return WebPageResult(
        url=url,
        title=title,
        text=_trim_text(text),
    )


if __name__ == "__main__":
    mcp.run()
