.PHONY: g_session claude_session sonnet opus haiku deslopp

# Desloppify — AI-driven code quality loop
# Override the agent with: make deslopp AGENT=cursor
AGENT ?= claude
MODEL ?= sonnet

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
	@echo -ne "\033]0;Claude: Sonnet\007"
	@claude --dangerously-skip-permissions --model "sonnet"

opus:
	@echo -ne "\033]0;Claude: Opus\007"
	@claude --dangerously-skip-permissions --model "opus"

haiku:
	@echo -ne "\033]0;Claude: Haiku\007"
	@claude --dangerously-skip-permissions --model "haiku"

g_session:
	gemini --approval-mode yolo