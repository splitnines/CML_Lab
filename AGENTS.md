# AGENTS.md

Guidance for coding agents working in this repository.

## 1) Scope and precedence
- This file applies to the repository rooted at `/home/rickey/cml_labs`.
- Instruction order: direct user request > this file > tool defaults.
- Keep edits focused and minimal; avoid unrelated refactors.
- Do not revert user-owned unrelated changes.

## 2) Repo shape (current state)
- This repo is mixed-purpose: network lab assets plus Python utilities.
- Main Python scripts at repo root: `cisco_ssh_mcp.py`, `cisco_web_mcp.py`.
- Python subprojects with `pyproject.toml`: `PKI-Troubleshooting/`, `SDWAN/`.
- There is no top-level `pyproject.toml` at the repository root.
- Assume Python target is 3.13+ where Python tooling is used.

## 3) Cursor/Copilot rule files
Checked for extra agent constraints in:
- `.cursor/rules/`
- `.cursorrules`
- `.github/copilot-instructions.md`

Current status: none of these files exist in this repository.

If these files appear later, treat them as additional constraints and update
this document.

## 4) Environment and setup
- Preferred toolchain for Python tasks: `uv`.
- For subprojects, run commands from that subproject directory.
- Typical setup in a Python project directory:
```bash
uv sync
```

## 5) Build/lint/type-check/test commands
There is no dedicated build artifact pipeline right now.
Use formatting, linting, typing, and tests as quality gates.

Run in the project directory that contains `pyproject.toml`.

Format:
```bash
uv run ruff format .
```

Lint:
```bash
uv run ruff check .
```

Lint with safe auto-fixes:
```bash
uv run ruff check . --fix
```

Type-check:
```bash
uv run ty check .
```

Full local quality pass:
```bash
uv run ruff format . && uv run ruff check . && uv run ty check .
```

## 6) Test execution (especially single-test)
No committed test suite is present right now, but use `pytest` conventions
for any new tests.

Run all tests:
```bash
uv run pytest -q
```

Run one test file:
```bash
uv run pytest tests/test_example.py -q
```

Run one test class:
```bash
uv run pytest tests/test_example.py::TestClassName -q
```

Run one specific test:
```bash
uv run pytest tests/test_example.py::TestClassName::test_case_name -q
```

Run tests by name pattern:
```bash
uv run pytest -k "keyword" -q
```

## 7) Running MCP scripts locally
From repo root (or equivalent script location):
Start SSH MCP server:
```bash
uv run python cisco_ssh_mcp.py
```

Start web MCP server:
```bash
uv run python cisco_web_mcp.py
```

## 8) Formatting and general style
- Max line length: 79 characters.
- Use Ruff formatter output as canonical style.
- Prefer ASCII unless file already requires Unicode.
- Keep functions small and readable; extract helpers when repeated logic appears.
- Avoid trailing whitespace and noisy formatting churn.
- Keep module-level constants uppercase and clearly named.

## 9) Imports and module structure
- Keep `from __future__ import annotations` first when used.
- Import groups order: standard library, third-party, local.
- Separate import groups with one blank line.
- Avoid wildcard imports.
- Remove unused imports and dead code.
- Prefer explicit imports over dynamic import tricks.

## 10) Typing and data modeling
- Add type hints for all function parameters and returns.
- Use built-in generics (`list[str]`, `dict[str, str]`).
- Prefer simple, readable types over advanced type-level constructs.
- Use `@dataclass` for structured return payloads where appropriate.
- Keep public function signatures stable unless change is requested.
- Ensure changes pass `uv run ty check .` in the relevant project folder.

## 11) Naming conventions
- Variables/functions: `snake_case`
- Classes/dataclasses: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private helper functions: prefix with `_`.
- Keep MCP tool names and argument shapes stable.

## 12) Error handling and control flow
- Validate external inputs early and fail fast.
- Raise specific, actionable errors (`ValueError` for invalid user input).
- Avoid broad `except Exception` unless re-raising with clear context.
- Close network/browser/session resources reliably (`try/finally`, context mgrs).
- Keep happy-path logic straightforward and easy to audit.
- Avoid swallowing exceptions silently.

## 13) Security and secrets
- Never hardcode passwords, tokens, cookies, or private keys.
- Read secrets from environment variables.
- Known env vars for SSH script: `IXC_USERNAME`, `IXC_PASSWORD`.
- Do not print sensitive values in logs, traces, or exception text.
- Preserve allowlist checks for external web access behavior.

## 14) Testing expectations for changes
- Add tests for non-trivial logic changes.
- Cover both success and failure paths.
- For bug fixes, add a regression test when practical.
- Keep tests deterministic, isolated, and fast.
- If no test exists for a touched area, call that out in your final report.

## 15) Change-management rules for agents
- Preserve public contracts unless user asks for a breaking change.
- Make targeted edits; do not rewrite unrelated files.
- Run relevant quality commands for changed code and report what ran.
- If commands cannot run locally, explain why and provide exact verify commands.
- Never commit or push unless the user explicitly requests it.
