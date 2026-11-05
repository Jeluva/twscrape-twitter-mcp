"""bookmarks tool: limit cap and empty result. Imports server, which needs deps installed."""

import asyncio

from twscrape_twitter_mcp import server


class _FakeApi:
    def __init__(self, n):
        self.n = n

    async def bookmarks(self, limit=-1):
        for i in range(self.n):
            yield i


def _fn(tool):
    return getattr(tool, "fn", tool)


def test_bookmarks_caps_to_limit(monkeypatch):
    monkeypatch.setattr(server, "get_api", lambda: _FakeApi(25))
    monkeypatch.setattr(server, "joined", lambda xs: ",".join(map(str, xs)))
    out = asyncio.run(_fn(server.bookmarks)(limit=3))
    assert out == "0,1,2"


def test_bookmarks_empty(monkeypatch):
    monkeypatch.setattr(server, "get_api", lambda: _FakeApi(0))
    out = asyncio.run(_fn(server.bookmarks)(limit=5))
    assert "No bookmarks" in out
