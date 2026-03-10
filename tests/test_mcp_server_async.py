"""Async tests for MCP server message loop and main."""

import asyncio
import json
from unittest.mock import MagicMock, patch

import pytest

from mad_frog.mcp_server import _message_loop
from mad_frog.mcp_server import main as mcp_main


def test_mcp_main_calls_serve():
    with patch("mad_frog.mcp_server.asyncio.run") as mock_run:
        mcp_main()
        mock_run.assert_called_once()


def test_dispatch_tool_call_exception():
    import mad_frog.mcp_server as mod

    original = mod.TOOL_HANDLERS.copy()
    mod.TOOL_HANDLERS["bad_tool"] = MagicMock(side_effect=RuntimeError("boom"))
    try:
        msg = {"jsonrpc": "2.0", "id": 10, "method": "tools/call", "params": {"name": "bad_tool"}}
        resp = mod._dispatch(msg)
        assert resp["result"]["isError"] is True
        assert "boom" in resp["result"]["content"][0]["text"]
    finally:
        mod.TOOL_HANDLERS.clear()
        mod.TOOL_HANDLERS.update(original)


@pytest.mark.asyncio
async def test_message_loop_full_handshake():
    """Test _message_loop processes initialize, notification, tools/list, tools/call."""
    messages = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "bmad_ping"}},
    ]
    input_bytes = "".join(json.dumps(m) + "\n" for m in messages).encode()

    reader = asyncio.StreamReader()
    reader.feed_data(input_bytes)
    reader.feed_eof()

    written = bytearray()

    def write_fn(data: bytes):
        written.extend(data)

    await _message_loop(reader, write_fn)

    lines = written.decode().strip().split("\n")
    assert len(lines) == 3  # initialize + tools/list + tools/call (notification has no response)

    resp1 = json.loads(lines[0])
    assert resp1["id"] == 1
    assert resp1["result"]["serverInfo"]["name"] == "mad-frog-bmad"

    resp2 = json.loads(lines[1])
    assert resp2["id"] == 2
    assert "bmad_ping" in [t["name"] for t in resp2["result"]["tools"]]

    resp3 = json.loads(lines[2])
    assert resp3["id"] == 3
    data = json.loads(resp3["result"]["content"][0]["text"])
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_message_loop_invalid_json():
    """Test _message_loop skips invalid JSON and continues processing."""
    init_msg = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    input_bytes = b"not json\n" + (init_msg + "\n").encode()

    reader = asyncio.StreamReader()
    reader.feed_data(input_bytes)
    reader.feed_eof()

    written = bytearray()
    await _message_loop(reader, lambda d: written.extend(d))

    lines = written.decode().strip().split("\n")
    assert len(lines) == 1
    resp = json.loads(lines[0])
    assert resp["id"] == 1


@pytest.mark.asyncio
async def test_message_loop_empty_input():
    """Test _message_loop exits cleanly on empty input (EOF)."""
    reader = asyncio.StreamReader()
    reader.feed_eof()

    written = bytearray()
    await _message_loop(reader, lambda d: written.extend(d))

    assert len(written) == 0
