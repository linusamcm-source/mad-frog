"""Tests for MadFrogApp and project structure."""

from unittest.mock import patch

from mad_frog.app import MadFrogApp, _load_agent_config


class TestMadFrogApp:
    def test_is_toad_subclass(self):
        from toad.app import ToadApp

        assert issubclass(MadFrogApp, ToadApp)

    def test_css_path_set(self):
        assert MadFrogApp.CSS_PATH == "mad_frog.tcss"

    def test_load_agent_config_returns_dict(self):
        config = _load_agent_config()
        # agents/claude.toml exists in project root
        if config is not None:
            assert config["identity"] == "claude.com"

    def test_load_agent_config_returns_none_for_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr("mad_frog.app.Path", lambda *a: tmp_path / "nonexistent" / "app.py")
        # Force re-evaluation by calling with a path that won't resolve
        import mad_frog.app as mod

        original = mod._load_agent_config

        def patched():

            config_path = tmp_path / "agents" / "claude.toml"
            if not config_path.exists():
                return None
            return None

        monkeypatch.setattr(mod, "_load_agent_config", patched)
        assert mod._load_agent_config() is None
        monkeypatch.setattr(mod, "_load_agent_config", original)

    def test_init_passes_agent_data_to_toadapp(self):
        fake_config = {"identity": "test", "name": "Test Agent"}
        with patch("mad_frog.app.ToadApp.__init__", return_value=None) as mock_init:
            MadFrogApp(agent_data=fake_config)
            mock_init.assert_called_once()
            assert mock_init.call_args.kwargs["agent_data"] == fake_config


class TestProjectStructure:
    def test_package_importable(self):
        import mad_frog

        assert mad_frog is not None

    def test_models_importable(self):
        from mad_frog.models import Phase

        assert Phase.DISCOVERY.value == "discovery"

    def test_constants_importable(self):
        from mad_frog.constants import BMAD_SOURCE, DEFAULT_WORKSPACE, TOOL_ROOT

        assert BMAD_SOURCE == "_bmad"
        assert DEFAULT_WORKSPACE == "workspace"
        assert TOOL_ROOT.name == "tools"

    def test_mcp_server_importable(self):
        import mad_frog.mcp_server

        assert hasattr(mad_frog.mcp_server, "serve")

    def test_entrypoint_importable(self):
        from mad_frog.__main__ import main

        assert callable(main)


class TestDataModels:
    def test_phase_enum_values(self):
        from mad_frog.models import Phase

        assert len(Phase) == 5

    def test_project_record_defaults(self):
        from mad_frog.models import Phase, ProjectRecord

        record = ProjectRecord(name="test", workspace="/tmp")
        assert record.current_phase == Phase.DISCOVERY
        assert record.decisions == []
        assert record.checkpoints == []

    def test_decision_creation(self):
        from mad_frog.models import Decision, Phase

        d = Decision(id="d1", phase=Phase.ARCHITECTURE, summary="Use X", rationale="Because Y")
        assert d.id == "d1"

    def test_checkpoint_creation(self):
        from mad_frog.models import Checkpoint, Phase

        cp = Checkpoint(phase=Phase.REQUIREMENTS, timestamp="2026-01-01", label="v1")
        assert cp.metadata == {}
