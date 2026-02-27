# AGENTS.md
This file defines conventions for coding agents working in this repository.

## 1) Project Context
- Language: Python (target `>=3.13`)
- Dependency/runtime tool: `uv`
- Primary libraries: `fastmcp`, `netmiko`, `playwright`
- Repo shape: flat root-level scripts, no `src/` package
- Main runtime units: two MCP servers

## 2) Repository Map
- `cisco_ssh_mcp.py` - Cisco SSH MCP tools
- `cisco_web_mcp.py` - Cisco web fetch MCP tool (Playwright)
- `pyproject.toml` - dependencies and Python constraints
- `uv.lock` - lockfile for reproducible installs
- `opencode.jsonc` - local MCP process wiring

## 3) Cursor/Copilot Rules Status
At analysis time, no repo-local rule files were found:
- `.cursor/rules/`
- `.cursorrules`
- `.github/copilot-instructions.md`
If these are added later, treat them as higher-priority instructions and
update this `AGENTS.md` accordingly.

## 4) Setup Commands
Use `uv` only.

Install/sync environment:
```bash
uv sync
```

## 5) Build/Lint/Test Commands
This repository currently has no separate build artifact step.
Use quality gates below instead.

Lint:
```bash
uv run ruff check .
```

Format:
```bash
uv run ruff format .
```

Type check:
```bash
uv run ty check .
```

Combined local quality pass:
```bash
uv run ruff format . && uv run ruff check . && uv run ty check .
```

### Tests (including single-test usage)
There are currently no committed pytest files, but use pytest when adding
tests.

Run full suite:
```bash
uv run pytest -q
```

Run one file:
```bash
uv run pytest tests/test_example.py -q
```

Run one specific test:
```bash
uv run pytest tests/test_example.py::test_case_name -q
```

Run one test class:
```bash
uv run pytest tests/test_example.py::TestClassName -q
```

Run by keyword expression:
```bash
uv run pytest -k "keyword" -q
```

## 6) Local Run Commands
Run SSH MCP server:
```bash
uv run python cisco_ssh_mcp.py
```

Run web MCP server:
```bash
uv run python cisco_web_mcp.py
```

## 7) Style and Architecture Rules

### 7.1 Formatting and files
- Enforce max line length of 79 chars.
- Use Ruff formatter as source of truth.
- Keep files ASCII unless existing file needs Unicode.

### 7.2 Imports
- Put `from __future__ import annotations` first when used.
- Import order: stdlib, third-party, local.
- Separate import groups with one blank line.
- Avoid wildcard imports.
- Remove dead imports.

### 7.3 Typing
- Type-annotate all function parameters and returns.
- Prefer built-in generic forms (e.g., `list[str]`).
- Use dataclasses for structured responses.
- Keep type annotations readable; avoid unnecessary complexity.
- Maintain compatibility with `ty check`.

### 7.4 Naming
- Functions and variables: `snake_case`.
- Classes/dataclasses: `PascalCase`.
- Constants: `UPPER_SNAKE_CASE`.
- Keep MCP tool names stable unless change is requested.

### 7.5 Error handling
- Validate external input early.
- Raise precise exceptions (typically `ValueError` for bad input).
- Provide concise, actionable error messages.
- Avoid broad `except Exception` unless needed for re-raise context.
- Ensure cleanup of network/browser/SSH resources on all code paths.

### 7.6 Security and secrets
- Never hardcode credentials/cookies/tokens.
- Read secrets from environment variables.
- Existing SSH vars: `IXC_USERNAME`, `IXC_PASSWORD`.
- Avoid printing sensitive values to logs/output.
- Preserve host allowlist checks for remote web access behavior.

### 7.7 Function design
- Prefer pure helper functions for normalization/parsing.
- Keep MCP tool handlers thin and easy to audit.
- Isolate side effects at boundaries (I/O, network calls).

### 7.8 Backward compatibility
- Treat MCP tool names/parameter shapes as public interfaces.
- Do not break output shapes without explicit request.

## 8) Testing Guidance for New Work
- Add tests for non-trivial logic additions.
- Cover both success and failure paths.
- Unit test helpers first; add integration tests where needed.
- For bug fixes, add a test that fails before the fix.

## 9) Agent Working Agreement
- Make minimal, targeted changes to satisfy the request.
- Do not refactor unrelated code opportunistically.
- After edits, run format + lint + type check.
- Run targeted tests when tests exist.
