"""MadFrogAgent — Agent subclass that injects the MCP server."""

from __future__ import annotations

# Work around circular import in toad.acp.agent ↔ toad.acp.messages
import toad.acp.messages  # noqa: F401
from toad.acp import api
from toad.acp.agent import Agent


class MadFrogAgent(Agent):
    async def acp_new_session(self) -> None:
        with self.request():
            session_new_response = api.session_new(
                str(self.project_root_path),
                [{"name": "mad-frog-bmad", "command": "python", "args": ["-m", "mad_frog.mcp_server"]}],
            )
        response = await session_new_response.wait()
        if response is None:
            raise RuntimeError("acp_new_session: session_new returned None")
        self.session_id = response["sessionId"]
