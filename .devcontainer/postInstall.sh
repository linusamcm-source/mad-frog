#!/usr/bin/env bash
set -euo pipefail
curl -fsSL https://claude.ai/install.sh | bash
echo "──────────────────────────────────────────"
echo " vibe_visualiser devcontainer — post-create setup"
echo "──────────────────────────────────────────"

# ── Desloppify ───────────────────────────────────────────────────────
if [ ! -d "$HOME/desloppify" ]; then
  git clone https://github.com/peteromallet/desloppify.git "$HOME/desloppify"
fi
pip install --upgrade "desloppify[full]"

# ── Fix volume ownership ────────────────────────────────────────────
# Docker creates named volumes as root — fix so 'vscode' user can write
for vol_dir in /workspace/node_modules /workspace/android; do
  if [ -d "$vol_dir" ] && [ "$(stat -c '%U' "$vol_dir")" != "vscode" ]; then
    echo "[0/4] Fixing ownership: $vol_dir"
    sudo chown vscode:vscode "$vol_dir"
  fi
done

# ── npm install ──────────────────────────────────────────────────────
if [ ! -f "node_modules/.package-lock.json" ] || \
   [ "package.json" -nt "node_modules/.package-lock.json" ]; then
  echo "[1/4] Installing npm dependencies..."
  npm install
else
  echo "[1/4] node_modules up to date, skipping install"
fi

# ── Expo prebuild (generates android/) ───────────────────────────────
echo "[2/4] Running Expo prebuild..."
npx expo prebuild --no-install 2>/dev/null || true

# ── AWS secrets (optional — only if credentials are mounted) ─────────
if [ -f "$HOME/.aws/credentials" ] || [ -f "$HOME/.aws/config" ]; then
  if [ -f "scripts/sync-secrets.sh" ] && [ ! -f ".env.local" ]; then
    echo "[3/4] Syncing secrets from AWS SSM..."
    bash scripts/sync-secrets.sh dev || echo "  Secrets sync failed (non-fatal)"
  else
    echo "[3/4] .env.local exists or no sync script, skipping secrets"
  fi
else
  echo "[3/4] No AWS credentials mounted, skipping secrets sync"
fi

# ── Fancy-git shell integration (optional — only if mounted) ────────
FANCY_GIT_DIR="$HOME/.fancy-git"
if [ -d "$FANCY_GIT_DIR" ]; then
  FANCY_GIT_SOURCE='[ -f "$HOME/.fancy-git/prompt.sh" ] && source "$HOME/.fancy-git/prompt.sh"'
  for rc_file in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [ -f "$rc_file" ] && ! grep -qF '.fancy-git/prompt.sh' "$rc_file"; then
      echo "" >> "$rc_file"
      echo "# Fancy-git prompt" >> "$rc_file"
      echo "$FANCY_GIT_SOURCE" >> "$rc_file"
      echo "  fancy-git: sourced in $(basename "$rc_file")"
    fi
  done
else
  echo "  fancy-git: not mounted, skipping"
fi

# ── Summary ──────────────────────────────────────────────────────────
echo "[4/4] Verifying toolchain..."
echo ""
echo "  Node:       $(node --version)"
echo "  npm:        $(npm --version)"
echo "  Python:     $(python --version)"
echo "  uv:         $(uv --version)"
echo "  Java:       $(java -version 2>&1 | head -1)"
echo "  Android SDK: ${ANDROID_HOME:-/opt/android-sdk}"
echo "  AWS CLI:    $(aws --version 2>&1 | cut -d' ' -f1)"
echo "  EAS CLI:    $(npx eas-cli --version 2>/dev/null || echo 'not found')"
echo ""

# ── ADB hint ─────────────────────────────────────────────────────────
cat <<'MSG'
──────────────────────────────────────────
 Ready.

 Quick start:
   npx expo start              # Metro bundler (scan QR from device)
   npx expo run:android        # Build + install via ADB

 Connecting to host emulator/device:
   1. On the HOST run:  adb -a nodaemon server
   2. Container uses ADB_SERVER_SOCKET=tcp:host.docker.internal:5037
   3. Verify:           adb devices

 AWS secrets:
   make sync-secrets            # Pull .env.local from SSM

──────────────────────────────────────────
MSG
