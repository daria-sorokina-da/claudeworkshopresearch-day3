# Claude Code Cheatsheet — Day 3

General Claude Code reference, pulled out of [EXERCISE.md](EXERCISE.md) so the lab
document stays focused on the repo and the task at hand. Nothing here is specific to
the Royal Stables lab — keep this tab open, or bookmark it for Monday.

---

## Commands and keyboard shortcuts worth having to hand

`/help` · `/plan` · `/rewind` · `/clear` · `/compact` · `/context` · `/usage` ·
`/cost` · `/init` · `/memory`

`Esc` — stop mid-run, keep context.
`Shift+Tab` — cycle approval modes.

## Mid-task side notes

While Claude is working, `/btw <note>` injects a correction without interrupting the
run — *`/btw use .temp not temp`* rather than stopping and re-prompting from scratch.

## Plan mode

`/plan` separates thinking from doing: Claude proposes an approach and you steer it in
plain language before anything gets written.

**Where do plan files go?** By default `~/.claude/plans/` (global, across every repo).
A repo can override this with `"plansDirectory": ".temp"` in `.claude/settings.json`,
so plans land beside other scratch files — gitignored, easy to find, gone when you're
done. (This repo sets it — see `.claude/settings.json`.)

## MCP configuration patterns

MCP (Model Context Protocol) is how Claude reaches tools beyond the filesystem and the
shell. Three ways it gets wired up, all exposing the same tool-call interface to
Claude — the difference is only where the server runs and how auth is handled:

| | Connector | Remote server | Local server |
|---|---|---|---|
| Example | Atlassian, GitHub | Context7 | a project's own `.mcp.json` server |
| Auth | OAuth via claude.ai | usually none | token / env var, or none |
| Configured in | claude.ai Settings → Integrations | `"type": "http"` in `.mcp.json` | `"command"` + `"args"` in `.mcp.json` |
| Runs where | Anthropic's cloud | provider's cloud | your machine |

## Context management

Run `/usage` to check how full the context window is. Past ~60%, `/compact` while
recall is still clean, before starting something that needs a lot of it.

## Further reading

- [code.claude.com/docs](https://code.claude.com/docs)
- [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)
- [Permissions reference](https://code.claude.com/docs/en/permissions)
- [anthropic.skilljar.com](https://anthropic.skilljar.com)
