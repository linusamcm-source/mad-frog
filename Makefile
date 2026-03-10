.PHONY: dev start test lint fmt deslopp sonnet opus haiku g_session bmad create-story dev-story code-review deslop-story

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

# deslopp:
# 	@desloppify update-skill $(AGENT)
# 	@desloppify scan --path .
# 	@claude --dangerously-skip-permissions --model $(MODEL) -p "\
# You are running the desloppify code quality improvement loop. \
# Run 'desloppify next' to get the next issue to fix. \
# Read the output carefully — it will tell you which file to edit and what to fix. \
# Implement the fix in the affected file. \
# Then run the resolve command shown by desloppify to mark it complete. \
# Repeat — run 'desloppify next', fix the issue, resolve it — until desloppify reports no more issues remaining. \
# Do not skip issues. Do not stop early."

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
	@claude --dangerously-skip-permissions --model opus "/bmad-agent-bmm-dev DS"

code-review:
	@claude --dangerously-skip-permissions --model opus "/bmad-agent-bmm-dev CR"


define DESLOP_PROMPT     
I want you to improve the quality of this codebase. To do this, install and run desloppify.
Run ALL of the following (requires Python 3.11+):

pip install --upgrade "desloppify[full]" 
desloppify update-skill claude # installs the full workflow guide — pick yours: claude, cursor, codex, copilot, windsurf, gemini

Before scanning, check for directories that should be excluded (vendor, build output,
generated code, worktrees, etc.) and exclude obvious ones with `desloppify exclude <path>`.
Share any questionable candidates with me before excluding.

desloppify scan --path .
desloppify next

--path is the directory to scan (use "." for the whole project, or "src/" etc).

Your goal is to get the strict score as high as possible. The scoring resists gaming — the
only way to improve it is to actually make the code better.

THE LOOP: run `next`. It tells you what to fix, which file, and the resolve command to run
when done. Fix it, resolve it, run `next` again. Over and over. This is your main job.

Don't be lazy. Large refactors and small detailed fixes — do both with equal energy. No task
is too big or too small. Fix things properly, not minimally.

Use `plan` to reorder priorities or cluster related issues. Rescan periodically. The scan
output includes agent instructions — follow them, don't substitute your own analysis."
endef
export DESLOP_PROMPT


deslop:
	@claude --dangerously-skip-permissions --model opus -p "$$DESLOP_PROMPT"

