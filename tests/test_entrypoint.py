"""Tests for __main__.py entrypoint."""

from unittest.mock import MagicMock, patch


class TestEntrypoint:
    def test_main_creates_and_runs_app(self):
        mock_app = MagicMock()
        with (
            patch("sys.argv", ["mad_frog"]),
            patch("mad_frog.app.MadFrogApp", return_value=mock_app),
        ):
            from mad_frog.__main__ import main

            main()
        mock_app.run.assert_called_once()

    def test_main_patches_conversation_agent(self):
        """Verify main() patches toad.widgets.conversation.Agent with MadFrogAgent."""
        mock_app = MagicMock()
        with (
            patch("sys.argv", ["mad_frog"]),
            patch("mad_frog.app.MadFrogApp", return_value=mock_app),
        ):
            from mad_frog.__main__ import main

            main()

        import toad.widgets.conversation as conv

        from mad_frog.agent import MadFrogAgent

        assert conv.Agent is MadFrogAgent

    def test_main_with_help_flag_exits(self):
        from mad_frog.__main__ import main

        with patch("sys.argv", ["mad_frog", "--help"]):
            try:
                main()
            except SystemExit as e:
                assert e.code == 0
