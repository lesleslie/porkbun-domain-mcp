# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-08-28

### Documentation

- readme: Bump Python badge from 3.13+ to 3.14+

### Internal

- Bump requires-python to >=3.14
- Bump version to 0.3.0
- Bump version to 0.3.0
- claude-md: Add oneiric action-kit discovery breadcrumb
- porkbun-domain-mcp: Bump tool-config pins from 3.13 to 3.14
- Re-pin python to 3.14

## [0.3.0] - 2026-08-21

### Added

- porkbun-domain-mcp: Adopt apply_tool_profile() (W4.6)
- porkbun-domain: Bodai plugin conversion (manifest, mcp.json, slash commands)

### Changed

- porkbun-domain-mcp: Fix W4.6 review Minors F2-F6

### Fixed

- porkbun-domain-mcp: Sort imports in test_doc_drift.py
- porkbun-domain-mcp: Sync version stamps (2026-08-19)

### Documentation

- porkbun-domain-mcp: Fix documented-but-not-wired audit findings (2026-08-19)
- porkbun-domain-mcp: Refresh stale test count (2026-08-19)

### Testing

- porkbun-domain-mcp: Add doc-drift CI guard (2026-08-19)
- porkbun-domain-mcp: Drive production lifespan in W4.3 test (W4.6 round 1 fix)

### Internal

- gitignore: Untrack .pyscn/ (bodai 2026-08-20)
- porkbun-domain-mcp: Bootstrap [tool.crackerjack] section + uv sync upgrade
- porkbun-domain-mcp: Gitignore .lycheecache (file, not just dir)
- porkbun-domain-mcp: Gitignore .lycheecache + .hypothesis
- porkbun-domain-mcp: Refresh crackerjack + oneiric deps
- porkbun-domain-mcp: Untrack .lycheecache + .hypothesis runtime artifacts

## [Unreleased]

### Added

- Tool profile dispatch via `apply_tool_profile()` from mcp-common 0.18.0
  (W4.6). New env var `PORKBUN_DOMAIN_TOOL_PROFILE` selects between
  `minimal` (health only), `standard` (all 5 tools), and `full` (default;
  same as pre-W4). The W0 `discover_tools` meta-tool is always present.
  See `docs/architecture/tool-profile-rationale.md` for the design.

### Internal

- Bump `mcp-common>=0.17.0` → `>=0.18.0` for the W0 profile dispatcher
- Refactor `porkbun_domain_mcp/server.py` to async `create_app()` +
  `create_app_sync()` shim so the W0 async dispatch helper can be awaited
  (the W2b.3 keystone — sync wrapper raises RuntimeError in event loops)
- Lifespan `finally` block now closes the same `PorkbunDomainClient`
  instance the registered tools use (the W4.3 reviewer finding — long-
  running servers leak httpx pools if the close call is dropped)
- Split `register_health_tool` + `register_domain_tools_for_profile` from
  the legacy `register_domain_tools` shim so the W0 dispatcher can
  register `health_check` independently at MINIMAL (the W4.1 reviewer
  finding)
- New `porkbun_domain_mcp/tools/profiles.py` (3-tier registration map +
  `_GROUP_REGISTRY` constant + bulk register fn)
- 32 new tests in `tests/unit/test_tool_profile.py` covering the W4
  contract (MINIMAL=health, async dispatch, caller-supplied settings,
  lifespan cleanup, AST guards that fail when `await` is removed)

## [0.2.1] - 2026-08-17

### Documentation

- Align README with 0.2.0 release and document lifecycle caveats

### Internal

- Untrack backup files (.backup, .backup.json, .bak)

## [0.2.0] - 2026-08-12

### Fixed

- Address ty errors
- Drop --cov-fail-under for empty test dir

### Internal

- Adopt register_http_health_route from mcp-common
- Bump oneiric dep to >=0.16.0
- Migrate MCPBaseSettings → OneiricMCPConfig, bump fastmcp to >=3.4.0,\<4
- Restore LICENSE and normalize attribution

## [0.1.4] - 2026-06-20

### Fixed

- Track .cache dir via .gitkeep for gitleaks support

### Internal

- Add mypy.ini and track .cache dir for quality tooling
- Untrack and delete 1 historical *.backup/*.bak files

## [0.1.2] - 2026-02-25

### Added

- Complete Porkbun Domain MCP server implementation

### Changed

- Update config, core

### Internal

- Update LICENSE copyright to 2026
