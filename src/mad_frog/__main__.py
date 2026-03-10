"""CLI entrypoint for Mad Frog."""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Mad Frog — guided BMAD planning")
    parser.parse_args()

    # Patch Toad's Conversation widget to use MadFrogAgent (injects MCP server config)
    import toad.widgets.conversation as _conv

    from mad_frog.agent import MadFrogAgent

    _conv.Agent = MadFrogAgent

    from mad_frog.app import MadFrogApp

    app = MadFrogApp()
    app.run()


if __name__ == "__main__":
    main()
