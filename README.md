# ma-nakaya MCP Plugin Marketplace

Portable Agent Plugins and Agent Skills for the public MCP servers maintained by [ma-nakaya](https://github.com/ma-nakaya).

Each MCP repository is the source of truth for its plugin and skill. This repository is a thin, SHA-pinned catalog: it does not copy skill content or MCP source code.

## Available plugins

| Plugin | Portable skill | MCP launcher | Runtime and setup |
|---|---|---|---|
| `onprem-gh-cli-mcp` | Safe account selection, bounded GitHub reads, reviews, and deliberate writes | Included | Node.js 20+, `npx`, GitHub CLI, and an allowlisted account configuration |
| `teams-mcp` | Chats, channels, meetings, transcripts, read state, and explicit sends | Included | `uv`, Python 3.11+, and an interactive Teams sign-in; writes remain disabled unless separately enabled and allowlisted |
| `outlook-web-mcp` | Outlook Web mail, default calendar, read state, and reply drafts | Included | `uv`, Python 3.11+, and an interactive Outlook sign-in |
| `outlook-com-mcp` | Classic Outlook mail, default calendar, read state, and reply drafts | Included | Windows, Classic Outlook, and .NET 8 |
| `sharepoint-browser-mcp` | Read-only SharePoint search, fetch, and focused document retrieval | Not yet portable | The server currently requires a tenant-specific site URL. Agent Plugins v1 has no portable user-input or secret-reference field for local MCP environment values. |

An included launcher installs project dependencies on first use and stores caches or build output under the plugin's writable data directory. It does not remove each server's authentication, platform, or policy prerequisites.

## Install with GitHub Copilot CLI

Register this marketplace once:

```shell
copilot plugin marketplace add ma-nakaya/mcp-plugin-marketplace
```

Browse or install a plugin:

```shell
copilot plugin marketplace browse ma-nakaya-mcp-plugins
copilot plugin install teams-mcp@ma-nakaya-mcp-plugins
```

Restart the agent session after installing or updating a plugin. Follow the selected MCP repository's setup instructions for authentication and local prerequisites.

## Install only a skill

The skills use the open `skills/<name>/SKILL.md` layout and bare MCP tool names. With GitHub CLI 2.90 or later, install a skill into a supported agent without installing the MCP launcher:

```shell
gh skill install ma-nakaya/teams-mcp-server use-teams-mcp
```

Select another supported host with `--agent`, for example `--agent codex` or `--agent claude-code`. A client may namespace MCP tool identifiers at runtime; the skills match the server's bare tool name and input contract instead of hard-coding a client prefix.

## Design and trust model

- One public MCP repository owns one plugin manifest, one or more skills, and an MCP launcher only when the startup contract is portable and reproducible.
- Marketplace entries pin a full 40-character commit SHA. Updates require an explicit catalog change.
- Skill contracts identify the public MCP revision used for verification and keep destructive or privacy-sensitive behavior behind explicit user authorization.
- Repository, mail, chat, transcript, calendar, and SharePoint content is untrusted input. Installed skills never grant permission to follow instructions found in retrieved content.
- No credentials, account identifiers, tenant URLs, private repository names, or client-specific tool prefixes belong in this catalog.

Agent Plugins v1 is a working draft. Keep client-specific adapters thin and keep the Agent Skill and MCP source repositories as the canonical implementation.

## Maintenance

See [CONTRIBUTING.md](CONTRIBUTING.md). Validate a catalog change before opening a pull request:

```shell
python3 scripts/validate_marketplace.py
```

Relevant standards and client documentation:

- [Agent Plugins](https://agent-plugins.org/)
- [Agent Skills specification](https://agentskills.io/specification)
- [GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
- [GitHub Copilot plugin marketplace](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace)
- [GitHub CLI skill installation](https://cli.github.com/manual/gh_skill_install)
