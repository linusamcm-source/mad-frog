"""Tests for MadFrogAgent."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mad_frog.agent import MadFrogAgent


class TestMadFrogAgent:
    def test_is_agent_subclass(self):
        from toad.acp.agent import Agent

        assert issubclass(MadFrogAgent, Agent)

    @pytest.mark.asyncio
    async def test_acp_new_session_injects_mcp_server(self):
        """Verify acp_new_session passes MCP server config to api.session_new."""
        agent = MadFrogAgent.__new__(MadFrogAgent)
        agent.project_root_path = "/tmp/test"

        mock_response = AsyncMock()
        mock_response.wait = AsyncMock(return_value={"sessionId": "test-123"})

        with (
            patch.object(agent, "request", return_value=MagicMock(__enter__=MagicMock(), __exit__=MagicMock())),
            patch("mad_frog.agent.api.session_new", return_value=mock_response) as mock_session_new,
        ):
            await agent.acp_new_session()

        mock_session_new.assert_called_once()
        args = mock_session_new.call_args
        assert args[0][0] == "/tmp/test"
        mcp_servers = args[0][1]
        assert len(mcp_servers) == 1
        assert mcp_servers[0]["name"] == "mad-frog-bmad"
        assert mcp_servers[0]["command"] == "python"
        assert "-m" in mcp_servers[0]["args"]
        assert "mad_frog.mcp_server" in mcp_servers[0]["args"]
        assert agent.session_id == "test-123"

    @pytest.mark.asyncio
    async def test_acp_new_session_raises_on_none_response(self):
        """Verify acp_new_session raises RuntimeError when session_new returns None."""
        agent = MadFrogAgent.__new__(MadFrogAgent)
        agent.project_root_path = "/tmp/test"

        mock_response = AsyncMock()
        mock_response.wait = AsyncMock(return_value=None)

        with (
            patch.object(agent, "request", return_value=MagicMock(__enter__=MagicMock(), __exit__=MagicMock())),
            patch("mad_frog.agent.api.session_new", return_value=mock_response),
        ):
            with pytest.raises(RuntimeError, match="session_new returned None"):
                await agent.acp_new_session()
