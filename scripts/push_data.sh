#!/usr/bin/env bash
# Commit data/relevant.jsonl and push it, surviving concurrent pushes (a human push while the bot runs).
# On a rebase conflict the data is rebuilt as the union of the remote file and the local database (import + export).
set -euo pipefail

git add data/relevant.jsonl
if git diff --cached --quiet; then echo "no new data"; exit 0; fi
MSG="data: update relevant articles ($(date -u '+%F %H:%M'))"
git commit -q -m "$MSG"

for attempt in 1 2 3; do
  git fetch -q origin main
  if git rebase origin/main >/dev/null 2>&1; then
    if git push -q origin HEAD:main; then echo "pushed (attempt $attempt)"; exit 0; fi
  else
    echo "rebase conflict: rebuilding union (attempt $attempt)"
    git rebase --abort || true
    git reset -q --hard origin/main
    uv run veille import
    uv run veille export
    git add data/relevant.jsonl
    if git diff --cached --quiet; then echo "remote already up to date"; exit 0; fi
    git commit -q -m "$MSG"
    if git push -q origin HEAD:main; then echo "pushed after rebuild (attempt $attempt)"; exit 0; fi
  fi
done
echo "could not push after 3 attempts" >&2
exit 1
