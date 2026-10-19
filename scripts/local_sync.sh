#!/usr/bin/env bash
# Fallback collector for the author's own machine (used only if GitHub's scheduler does not fire).
# Same pipeline as the GitHub workflow, safe to run alongside it thanks to push_data.sh.
set -euo pipefail
cd "$(dirname "$0")/.."
git pull -q --rebase origin main
uv run veille import
uv run veille collect --days 2
uv run veille export
bash scripts/push_data.sh
