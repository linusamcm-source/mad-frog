.PHONY: dev start test lint fmt deslopp sonnet opus haiku g_session bmad create-story dev-story code-review

# === Core targets ===

dev:
	uv sync

start:
	uv run mad_frog

test:
	uv run pytest --cov --cov-report=term-missing

lint:
	uv run ruff check src/ tests/

fmt:
	uv run ruff format src/ tests/

# === AI agent shortcuts ===

AGENT ?= claude
MODEL ?= opus

deslopp:
	@desloppify update-skill $(AGENT)
	@desloppify scan --path .
	@claude --dangerously-skip-permissions --model $(MODEL) -p "\
You are running the desloppify code quality improvement loop. \
Run 'desloppify next' to get the next issue to fix. \
Read the output carefully — it will tell you which file to edit and what to fix. \
Implement the fix in the affected file. \
Then run the resolve command shown by desloppify to mark it complete. \
Repeat — run 'desloppify next', fix the issue, resolve it — until desloppify reports no more issues remaining. \
Do not skip issues. Do not stop early."

sonnet:
	@claude --dangerously-skip-permissions --model "sonnet"

opus:
	@claude --dangerously-skip-permissions --model "opus"

haiku:
	@claude --dangerously-skip-permissions --model "haiku"

g_session:
	gemini --approval-mode yolo

bmad:
	@npx bmad-method install

create-story:
	@claude --dangerously-skip-permissions --model opus "/bmad-agent-bmm-sm  CS"

dev-story:
	@claude --dangerously-skip-permissions --model opus "/bmad-agent-bmm-dev DS" _bmad-output/implementation-artifacts/repos/toad.xml

code-review:
	@claude --dangerously-skip-permissions --model opus "/bmad-agent-bmm-dev CR"
