#!/usr/bin/env bash


set -euo pipefail

# Ensure ~/.local/bin is on PATH for tools installed during this script
export PATH="$HOME/.local/bin:$PATH"

echo "──────────────────────────────────────────"
echo " vibe_visualiser devcontainer — post-create setup"
echo "──────────────────────────────────────────"

# ── Git identity (fall back to env vars if host .gitconfig not mounted) ──
if ! git config --global user.name &>/dev/null; then
  if [ -n "${GIT_USER_NAME:-}" ]; then
    git config --global user.name "$GIT_USER_NAME"
  fi
fi
if ! git config --global user.email &>/dev/null; then
  if [ -n "${GIT_USER_EMAIL:-}" ]; then
    git config --global user.email "$GIT_USER_EMAIL"
  fi
fi
if ! git config --global user.name &>/dev/null || ! git config --global user.email &>/dev/null; then
  echo "  WARNING: Git identity not configured."
  echo "  Set GIT_USER_NAME and GIT_USER_EMAIL env vars, or ensure ~/.gitconfig exists on host."
fi

# ── Claude  ────────
curl -fsSL https://claude.ai/install.sh | bash || echo "  WARNING: Claude install failed, continuing..."

# ── Bun (needed by ccstatusline) ────────
if ! command -v bun &>/dev/null; then
  echo "Installing Bun..."
  curl -fsSL https://bun.sh/install | bash || echo "  WARNING: Bun install failed, continuing..."
  export PATH="$HOME/.bun/bin:$PATH"
  for rc in "$HOME/.bashrc" "$HOME/.profile"; do
    if ! grep -q '\.bun/bin' "$rc" 2>/dev/null; then
      echo 'export PATH="$HOME/.bun/bin:$PATH"' >> "$rc"
    fi
  done
fi

# ---install ccstatusline-------
echo "Installing ccstatusline..."
mkdir -p "$HOME/.config/ccstatusline"
cp "$(dirname "$0")/ccstatusline-settings.json" "$HOME/.config/ccstatusline/settings.json"

# ── Toad  ────────
echo "Installing Toad ..."
curl -fsSL https://batrachian.ai/install | sh || echo "  WARNING: Toad install failed, continuing..."

# ── Fancy-git  ────────
echo "Installing Fancy-git..."
curl -sS https://raw.githubusercontent.com/diogocavilha/fancy-git/master/install.sh | sh || echo "  WARNING: Fancy-git install failed, continuing..."


echo "Installing Python Packages with UV..."
if [ ! -f "pyproject.toml" ]; then
  uv init
fi
uv add ruff bandit safety vulture pydantic desloppify[full] loguru pytest pytest-cov pre-commit
uv lock
uv sync

# Ensure ~/.local/bin is on PATH for uv-installed tools
export PATH="$HOME/.local/bin:$PATH"
for rc in "$HOME/.bashrc" "$HOME/.profile"; do
  if ! grep -q '\.local/bin' "$rc" 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$rc"
  fi
done
# ── Desloppify ───────────────────────────────────────────────────────
if [ ! -d "$HOME/desloppify" ]; then
  git clone https://github.com/peteromallet/desloppify.git "$HOME/desloppify" || echo "  WARNING: Desloppify clone failed, continuing..."
fi

# ── Fancy-git shell integration (source prompt if installed) ────────
FANCY_GIT_DIR="$HOME/.fancy-git"
if [ -d "$FANCY_GIT_DIR" ]; then
  FANCY_GIT_SOURCE='[ -f "$HOME/.fancy-git/prompt.sh" ] && source "$HOME/.fancy-git/prompt.sh"'
  for rc_file in "$HOME/.bashrc"; do
    if [ -f "$rc_file" ] && ! grep -qF '.fancy-git/prompt.sh' "$rc_file"; then
      echo "" >> "$rc_file"
      echo "# Fancy-git prompt" >> "$rc_file"
      echo "$FANCY_GIT_SOURCE" >> "$rc_file"
      echo "  fancy-git: sourced in $(basename "$rc_file")"
    fi
  done
else
  echo "  fancy-git: not installed, skipping prompt integration"
fi

# ── BMAD ──────────────────────────────────────────────────────────
echo "Installing BMAD..."
if [ -d "$(pwd)/_bmad-output" ]; then
  echo "  BMAD already installed, running quick-update..."
  npx --yes bmad-method install \
    --directory "$(pwd)" \
    --action quick-update
else
  npx --yes bmad-method install \
    --directory "$(pwd)" \
    --modules bmm,bmb \
    --tools claude-code,gemini  \
    --user-name "$USER" \
    --communication-language English \
    --document-output-language English \
    --output-folder _bmad-output \
    --yes
fi

repomix --remote https://github.com/batrachianai/toad.git --compress -o _bmad-output/implementation-artifacts/repos/toad.xml 
repomix --remote https://github.com/bmad-code-org/BMAD-METHOD.git --compress -o _bmad-output/implementation-artifacts/repos/bmad-method.xml 

unzip -o /workspaces/mad-frog/.devcontainer/fancy-git.zip -d ~ 

# ── Summary ──────────────────────────────────────────────────────────
echo "Final - Verifying toolchain..."
echo ""
echo "  Node:       $(node --version)"
echo "  npm:        $(npm --version)"
echo "  Python:     $(python --version)"
echo "  uv:         $(uv --version)"
echo "  toad:       $(toad --version)"
echo "  Java:       $(java -version 2>&1 | head -1)"
echo ""
# ── ADB hint ─────────────────────────────────────────────────────────
cat <<'MSG'
──────────────────────────────────────────
 Ready.
 Quick start:
   make start             # Start the development server

──────────────────────────────────────────
MSG
