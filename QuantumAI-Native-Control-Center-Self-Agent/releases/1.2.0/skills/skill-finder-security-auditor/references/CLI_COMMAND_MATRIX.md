# CLI command contract
| Action | Official CLI | Mutation | Default |
|---|---|---|---|
| Prerequisites | `node --version`, `npx --version` | no | preflight |
| Search | `DISABLE_TELEMETRY=1 npx skills find <query>` | remote lookup, cache possible | with suitable provider |
| List | `DISABLE_TELEMETRY=1 npx skills list -g` | no intended skill mutation | allowed |
| Check | `DISABLE_TELEMETRY=1 npx skills check` | no intended skill mutation | allowed |
| Install | `DISABLE_TELEMETRY=1 npx skills add vercel-labs/skills --skill find-skills -g -a claude-code --copy -y` | yes | separate approval |
| Update | `DISABLE_TELEMETRY=1 npx skills update -g` | yes | separate approval |
| Remove | `DISABLE_TELEMETRY=1 npx skills remove find-skills` | yes | BLOCKED absent separate approval |
| Try | `DISABLE_TELEMETRY=1 npx skills use <repo>@<skill>` | fetch and agent launch possible | inspect only; no untrusted execution |

Pinned source commits and lock file hashes are preferred for reproducibility. Flags must be confirmed with the actual installed CLI. Node >=22.20 is enforced by preflight before install. Confirm that `$HOME/.claude/skills/find-skills/SKILL.md` is a regular file when `--copy` is requested; do not replace an existing symlink.
