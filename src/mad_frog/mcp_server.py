"""Lightweight stdio MCP server — newline-delimited JSON-RPC over stdin/stdout.

CRITICAL: Never write to stdout except JSON-RPC responses.
All logging goes to stderr.
"""

import asyncio
import json
import logging
import sys

from mad_frog.tools.ping import BMAD_PING_TOOL, handle_bmad_ping

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format="%(name)s %(message)s")
log = logging.getLogger("mcp")

SERVER_INFO = {
    "name": "mad-frog-bmad",
    "version": "0.1.0",
}

CAPABILITIES = {"tools": {"listChanged": False}}

TOOLS = [BMAD_PING_TOOL]

TOOL_HANDLERS = {
    "bmad_ping": handle_bmad_ping,
}


def _jsonrpc_response(req_id, result):
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def _jsonrpc_error(req_id, code, message):
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


def _dispatch(msg: dict) -> dict | None:
    method = msg.get("method", "")
    req_id = msg.get("id")
    params = msg.get("params", {})

    if method == "initialize":
        result = {
            "protocolVersion": "2024-11-05",
            "capabilities": CAPABILITIES,
            "serverInfo": SERVER_INFO,
        }
        return _jsonrpc_response(req_id, result)

    if method == "notifications/initialized":
        return None  # notification — no response

    if method == "tools/list":
        return _jsonrpc_response(req_id, {"tools": TOOLS})

    if method == "tools/call":
        tool_name = params.get("name", "")
        handler = TOOL_HANDLERS.get(tool_name)
        if handler is None:
            return _jsonrpc_error(req_id, -32601, f"Unknown tool: {tool_name}")
        try:
            result = handler()
        except Exception as exc:
            return _jsonrpc_response(
                req_id,
                {"content": [{"type": "text", "text": f"Error: {exc}"}], "isError": True},
            )
        return _jsonrpc_response(req_id, result)

    return _jsonrpc_error(req_id, -32601, f"Method not found: {method}")


async def _message_loop(reader: asyncio.StreamReader, write_fn) -> None:
    """Read JSON-RPC messages from reader, dispatch, write responses via write_fn."""
    while True:
        line = await reader.readline()
        if not line:
            break
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            log.warning("Invalid JSON: %s", line)
            continue

        log.debug("← %s", msg.get("method", "?"))
        response = _dispatch(msg)

        if response is not None:
            payload = json.dumps(response) + "\n"
            write_fn(payload.encode())
            log.debug("→ response id=%s", response.get("id"))


async def serve() -> None:
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    loop = asyncio.get_running_loop()
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)

    transport, _ = await loop.connect_write_pipe(asyncio.Protocol, sys.stdout)

    log.info("MCP server started on stdio")
    await _message_loop(reader, transport.write)


def main() -> None:
    asyncio.run(serve())


if __name__ == "__main__":
    main()
