#!/bin/bash
set -euo pipefail
MODE="${1:---dry-run}"
case "$MODE" in --dry-run|--install|--uninstall|--status) ;; *) echo 'Usage: install_launchagent.sh --dry-run|--install|--uninstall|--status' >&2; exit 2;; esac
if [[ "$(uname -s)" != 'Darwin' ]]; then echo 'BLOCKED: macOS required' >&2; exit 3; fi
SELF="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd -P)"
PYTHON="$(command -v python3 || true)"
LABEL='com.quantumai.native-control-center.readonly'
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
OUT="$HOME/Library/Logs/QuantumAI-Native-Control-Center"
if [[ "$MODE" == '--dry-run' ]]; then printf 'READ_ONLY installation plan: %s -> %s\n' "$SELF" "$PLIST"; exit 0; fi
if [[ "$MODE" == '--status' ]]; then launchctl list "$LABEL" 2>&1 || :; exit 0; fi
if [[ "$MODE" == '--uninstall' ]]; then
  if [[ -f "$PLIST" ]]; then launchctl bootout "gui/$(id -u)" "$PLIST" 2>/dev/null || :; rm -- "$PLIST"; fi
  echo 'Only this LaunchAgent configuration was removed; reports remain.'
  exit 0
fi
[[ -n "$PYTHON" && -f "$SELF/scripts/control_center.py" ]] || { echo 'BLOCKED: missing Python or script'; exit 3; }
mkdir -p "$HOME/Library/LaunchAgents" "$OUT"
[[ ! -e "$PLIST" ]] || { echo "BLOCKED: existing plist preserved: $PLIST" >&2; exit 4; }
# PLIST paths are injected through Python plistlib to ensure XML escaping.
"$PYTHON" - "$PLIST" "$PYTHON" "$SELF/scripts/control_center.py" "$OUT" "$LABEL" <<'PY2'
import pathlib,plistlib,sys
plist,exe,script,out,label=sys.argv[1:]
obj={'Label':label,'ProgramArguments':[exe,script,'observe','--output',out+'/latest.json'], 'StartInterval':3600,'RunAtLoad':True,'StandardOutPath':out+'/stdout.log','StandardErrorPath':out+'/stderr.log','ProcessType':'Background'}
with open(plist,'xb') as f: plistlib.dump(obj,f)
PY2
plutil -lint "$PLIST"
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "Installed read-only LaunchAgent: $PLIST"
