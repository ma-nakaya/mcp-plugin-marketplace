# Catalog maintenance instructions

- Treat `.github/plugin/marketplace.json` as the catalog source of truth.
- Do not copy MCP source or per-MCP skills into this repository. Change the owning public MCP repository first.
- Every marketplace plugin source must be a public `ma-nakaya` repository pinned to a full 40-character commit SHA.
- Verify that the pinned commit contains a root `plugin.json` and at least one `skills/*/SKILL.md` before updating the catalog.
- Do not add `mcp.json` to a plugin source unless its launcher is portable, uses no embedded credential or private identifier, and writes runtime data only under `${PLUGIN_DATA}`.
- Preserve exact source licenses. Do not add a license field when the source repository has no declared license.
- Run `python3 scripts/validate_marketplace.py` after every catalog change.
- Never publish credentials, tenant URLs, account identifiers, private repository names, private conversation data, or client-specific MCP tool prefixes.
