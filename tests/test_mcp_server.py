"""Tests for the MCP server dispatch logic."""

import json

from mad_frog.mcp_server import _dispatch


class TestInitialize:
    def test_returns_capabilities(self):
        msg = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        resp = _dispatch(msg)
        assert resp["id"] == 1
        result = resp["result"]
        assert result["capabilities"]["tools"]["listChanged"] is False
        assert result["serverInfo"]["name"] == "mad-frog-bmad"
        assert result["protocolVersion"] == "2024-11-05"


class TestNotificationsInitialized:
    def test_returns_none(self):
        msg = {"jsonrpc": "2.0", "method": "notifications/initialized"}
        assert _dispatch(msg) is None


class TestToolsList:
    def test_returns_bmad_ping(self):
        msg = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
        resp = _dispatch(msg)
        tools = resp["result"]["tools"]
        assert len(tools) >= 1
        names = [t["name"] for t in tools]
        assert "bmad_ping" in names


class TestToolsCall:
    def test_bmad_ping_returns_ok(self):
        msg = {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "bmad_ping"}}
        resp = _dispatch(msg)
        result = resp["result"]
        assert result["isError"] is False
        data = json.loads(result["content"][0]["text"])
        assert data["status"] == "ok"
        assert data["version"] == "0.1.0"

    def test_unknown_tool_returns_error(self):
        msg = {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "nonexistent"}}
        resp = _dispatch(msg)
        assert resp["error"]["code"] == -32601


class TestInvalidMethod:
    def test_unknown_method_returns_error(self):
        msg = {"jsonrpc": "2.0", "id": 5, "method": "foo/bar", "params": {}}
        resp = _dispatch(msg)
        assert resp["error"]["code"] == -32601
        assert "foo/bar" in resp["error"]["message"]
