"""Tests for MCP server process lifecycle — startup and graceful shutdown."""

import json
import subprocess
import sys
import time


class TestMCPServerProcess:
    def test_server_starts_and_responds(self):
        """Start MCP server as subprocess, send initialize, verify response."""
        proc = subprocess.Popen(
            [sys.executable, "-m", "mad_frog.mcp_server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            msg = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}) + "\n"
            proc.stdin.write(msg.encode())
            proc.stdin.flush()

            # Read response
            line = proc.stdout.readline()
            assert line, "No response from MCP server"

            resp = json.loads(line)
            assert resp["id"] == 1
            assert resp["result"]["serverInfo"]["name"] == "mad-frog-bmad"
        finally:
            proc.terminate()
            proc.wait(timeout=3)

    def test_graceful_shutdown_on_stdin_close(self):
        """Server should exit cleanly when stdin is closed."""
        proc = subprocess.Popen(
            [sys.executable, "-m", "mad_frog.mcp_server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        proc.stdin.close()
        exit_code = proc.wait(timeout=5)
        assert exit_code == 0

    def test_graceful_shutdown_on_sigterm(self):
        """Server should exit within 2 seconds on SIGTERM."""
        import signal

        proc = subprocess.Popen(
            [sys.executable, "-m", "mad_frog.mcp_server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(0.3)  # let server start
        proc.send_signal(signal.SIGTERM)
        start = time.monotonic()
        proc.wait(timeout=5)
        elapsed = time.monotonic() - start
        assert elapsed < 2, f"Shutdown took {elapsed:.1f}s, expected <2s"

    def test_tools_list_roundtrip(self):
        """Full handshake: initialize → notifications/initialized → tools/list."""
        proc = subprocess.Popen(
            [sys.executable, "-m", "mad_frog.mcp_server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            # initialize
            msg = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}) + "\n"
            proc.stdin.write(msg.encode())
            proc.stdin.flush()
            proc.stdout.readline()  # consume response

            # notifications/initialized (no response expected)
            msg = json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n"
            proc.stdin.write(msg.encode())
            proc.stdin.flush()

            # tools/list
            msg = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}) + "\n"
            proc.stdin.write(msg.encode())
            proc.stdin.flush()
            line = proc.stdout.readline()
            resp = json.loads(line)
            tool_names = [t["name"] for t in resp["result"]["tools"]]
            assert "bmad_ping" in tool_names
        finally:
            proc.terminate()
            proc.wait(timeout=3)
