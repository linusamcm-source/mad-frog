.PHONY: g_session claude_session sonnet opus haiku deslopp

# Desloppify — AI-driven code quality loop
# Override the agent with: make deslopp AGENT=cursor
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

start:
	@echo "Starting development process..."
	@toad


#   1. Validate the PRD — run /bmad-bmm-validate-prd to check for gaps, anti-patterns, and implementation readiness
#   2. Create UX Design — run /bmad-bmm-create-ux-design to translate user journeys into interaction flows
#   3. Create Architecture — run /bmad-bmm-create-architecture to make technical design decisions informed by FRs and NFRs
#   4. Check Implementation Readiness — run /bmad-bmm-check-implementation-readiness to verify all artifacts are complete before breaking into epics