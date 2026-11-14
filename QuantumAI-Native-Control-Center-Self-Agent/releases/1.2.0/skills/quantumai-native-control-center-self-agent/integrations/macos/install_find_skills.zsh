#!/bin/zsh
set -euo pipefail
MODE="${1:---preflight}"
ROOT="${0:A:h:h:h}"
FINDER="$ROOT/../skill-finder-security-auditor/scripts/find_skills_manager.py"
[[ -f "$FINDER" ]] || { echo "BLOCKED: skill manager missing: $FINDER" >&2; exit 3; }
command -v python3 >/dev/null || { echo 'BLOCKED: python3 required' >&2; exit 3; }
case "$MODE" in
  --preflight|--plan) python3 "$FINDER" "${MODE#--}" ;;
  --install)
    python3 "$FINDER" preflight >/dev/null || { echo 'BLOCKED: prerequisites' >&2; exit 3; }
    TARGET="$HOME/.claude/skills/find-skills"
    if [[ -e "$TARGET" || -L "$TARGET" ]]; then echo "BLOCKED: existing installation preserved: $TARGET" >&2; exit 4; fi
    [[ "${QAI_FIND_SKILLS_SOURCE_REVIEWED:-}" == '1' && "${QAI_FIND_SKILLS_INSTALL_AUTHORIZED:-}" == '1' ]] || {
      echo 'BLOCKED: source review and explicit installation authorization required' >&2; exit 5;
    }
    command -v npx >/dev/null || exit 6
    DISABLE_TELEMETRY=1 npx skills add vercel-labs/skills --skill find-skills -g -a claude-code --copy -y
    python3 "$FINDER" verify --path "$TARGET/SKILL.md"
    DISABLE_TELEMETRY=1 npx skills list -g
    ;;
  *) echo 'Usage: install_find_skills.zsh --preflight|--plan|--install' >&2; exit 2;;
esac
