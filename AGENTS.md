# AGENTS.md

Guidance for coding agents working in `/home/rickey/cml_labs`.

## 1) Scope and precedence
- Applies to the repository rooted at `/home/rickey/cml_labs`.
- Precedence: direct user request > nearest `AGENTS.md` > this file.
- Nested folders may define stricter local rules.
- Example: `Containers/pki-server/AGENTS.md` overrides this file in that
  subtree.
- Keep edits minimal, task-focused, and operationally safe.
- Never revert unrelated user-owned changes.

## 2) Repository map (current state)
- Mixed-purpose repo: network lab assets + Python utilities.
- Root scripts:
  - `cisco_ssh_mcp.py`
  - `cisco_web_mcp.py`
- Python subprojects with `pyproject.toml`:
  - `PKI-Troubleshooting/`
  - `SDWAN/`
- No top-level `pyproject.toml` exists at repo root.
- Python target is 3.13+ where Python tooling is used.

## 3) Cursor/Copilot rule files
Checked for additional constraints in:
- `.cursor/rules/`
- `.cursorrules`
- `.github/copilot-instructions.md`

Current status: none of these files exist in this repository.

If they are added later, treat them as active instructions and update this
document.

## 4) Environment and setup
- Use `uv` for Python dependency management and command execution.
- Run commands from the directory that contains the target `pyproject.toml`.
- Typical setup in each Python subproject:

```bash
uv sync
```

## 5) Build/lint/type/test commands
There is no dedicated build artifact pipeline. Use format/lint/type/test as
quality gates.

### PKI-Troubleshooting
Run from `/home/rickey/cml_labs/PKI-Troubleshooting`:

```bash
uv run ruff format .
uv run ruff check .
uv run ruff check . --fix
uv run ty check .
uv run pytest -q
```

### SDWAN
Run from `/home/rickey/cml_labs/SDWAN`:

```bash
uv run ruff format .
uv run ruff check .
uv run ruff check . --fix
uv run ty check .
uv run pytest -q
```

### Full local quality pass (Python subproject)

```bash
uv run ruff format . && uv run ruff check . && uv run ty check .
```

## 6) Single-test commands (important)
Use `pytest` node selectors for targeted execution:

```bash
uv run pytest tests/test_example.py -q
uv run pytest tests/test_example.py::TestClassName -q
uv run pytest tests/test_example.py::TestClassName::test_case_name -q
uv run pytest -k "keyword" -q
```

## 7) Running root MCP scripts
From `/home/rickey/cml_labs`:

```bash
uv run python cisco_ssh_mcp.py
uv run python cisco_web_mcp.py
```

## 8) Formatting and code style
- Max line length: 79 characters.
- Use Ruff formatter output as canonical style.
- Prefer ASCII unless file content already requires Unicode.
- Keep functions focused and readable.
- Extract helpers when logic repeats.
- Avoid noisy formatting-only churn in unrelated files.
- Keep constants in `UPPER_SNAKE_CASE`.

## 9) Imports
- If used, keep `from __future__ import annotations` at the top.
- Group imports: standard library, third-party, local.
- Separate groups with one blank line.
- Avoid wildcard imports.
- Remove unused imports promptly.
- Prefer explicit imports over dynamic import patterns.

## 10) Typing
- Add type hints to function parameters and return values.
- Use built-in generics (`list[str]`, `dict[str, str]`).
- Prefer simple, readable types over complex type-level tricks.
- Use `@dataclass` for structured payloads when helpful.
- Keep public signatures stable unless user requests a change.
- Run `uv run ty check .` in the touched Python subproject.

## 11) Naming conventions
- Variables/functions: `snake_case`.
- Classes: `PascalCase`.
- Constants: `UPPER_SNAKE_CASE`.
- Private helpers: leading underscore (`_helper_name`).
- Keep MCP tool names and argument schemas stable.

## 12) Error handling
- Validate external inputs early and fail fast.
- Raise specific exceptions with actionable messages.
- Avoid broad `except Exception` unless re-raising with context.
- Never swallow exceptions silently.
- Close resources reliably (`with`, `try/finally`).
- Keep happy-path logic straightforward and auditable.

## 13) Security and secrets
- Never hardcode passwords, tokens, cookies, or private keys.
- Read secrets from environment variables.
- Known env vars: `IXC_USERNAME`, `IXC_PASSWORD`.
- Never print sensitive values in logs, traces, or error text.
- Preserve existing allowlist/safety checks for outbound actions.

## 14) Testing expectations
- Add tests for non-trivial behavior changes.
- Cover success and failure paths.
- Add regression tests for bug fixes when practical.
- Keep tests deterministic, isolated, and fast.
- If no tests exist for touched code, state that clearly in your report.

## 15) Infra/docs safety in this repo
- Some directories are operational lab assets (for example
  `Containers/pki-server`).
- In operational areas, prefer minimal reversible edits.
- Use validation commands from the nearest local `AGENTS.md`.
- Never expose or commit secrets from CA/state directories or archives.

## 16) Change-management rules
- Preserve public behavior unless breaking change is requested.
- Keep edits scoped; avoid unrelated cleanup.
- Run relevant verification commands and report outcomes.
- If verification cannot be run, explain why and give exact commands.
- Do not commit or push unless the user explicitly asks.
