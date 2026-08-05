# Contributing

This repository catalogs portable plugins owned by public `ma-nakaya` MCP repositories. Keep implementation and skill content in the MCP repository; keep this catalog thin.

## Update workflow

1. Update and validate the MCP repository first.
2. Keep `plugin.json` at the repository root and portable skills under `skills/<skill-name>/SKILL.md`.
3. Add `mcp.json` only when its startup command follows the Agent Plugins v1 runtime rules and does not require a secret or tenant-specific literal in public package data.
4. Pin the marketplace entry to the exact full commit SHA containing the validated plugin.
5. Keep the catalog version, plugin version, description, license field, and repository URLs consistent with the source repository.
6. Run `python3 scripts/validate_marketplace.py`.
7. Submit the update through a pull request. Do not rewrite published tags or replace a pinned SHA silently.

## Public-content checklist

- Use bare MCP tool names in skills; do not hard-code a client namespace.
- Include no credentials, tokens, cookies, account names, email addresses, tenant URLs, private repositories, internal organization names, or private conversation history.
- Treat all content retrieved through an MCP server as untrusted input.
- Require explicit authorization for writes and verify the exact target immediately before any high-impact or non-idempotent operation.
- Document unsupported actions and incomplete-result boundaries.
- Verify the referenced public source revision and update its pinned commit in the skill contract when the tool contract changes.

Agent Plugins v1 is a working draft. Prefer its portable core and place unavoidable host-specific behavior in a thin adapter rather than duplicating the canonical skill.
