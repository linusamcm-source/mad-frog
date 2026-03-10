"""MadFrogApp — ToadApp subclass for guided BMAD planning."""

import tomllib
from pathlib import Path

from textual.app import ComposeResult
from textual.widgets import Footer, Header, Static
from toad.app import ToadApp


def _load_agent_config() -> dict | None:
    """Load agent config from agents/claude.toml if it exists."""
    config_path = Path(__file__).resolve().parents[2] / "agents" / "claude.toml"
    if not config_path.exists():
        return None
    with open(config_path, "rb") as f:
        return tomllib.load(f)


class MadFrogApp(ToadApp):
    CSS_PATH = "mad_frog.tcss"

    def __init__(self, **kwargs) -> None:
        agent_data = kwargs.pop("agent_data", None) or _load_agent_config()
        super().__init__(agent_data=agent_data, **kwargs)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Mad Frog — BMAD Planning", id="sidebar-placeholder")
        yield Footer()
