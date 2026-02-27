# AGENTS.md

Guidance for coding agents operating in
`/home/rickey/cml_labs/Containers/pki-server`.

## Scope
- Dockerized `smallstep/step-ca` for lab PKI and Cisco SCEP.
- Mostly infra + docs (`docker-compose.yml`, `*.md`).
- Treat as potentially live CA data; prefer minimal, reversible edits.

## Environment
- Main host: `10.0.0.149` (SSH via existing `ssh-agent`).
- Container name: `step-ca`.
- Host path: `~/Containers/pki-server`.
- Bind mount: `./step` (host) -> `/home/step` (container).

## Key files
- `docker-compose.yml`: ports, env vars, healthcheck.
- `README.md`: runbook, migration, IP change procedures.
- `PROBLEM.md`, `SOLUTION.md`, `STEP_CA_SAN_LOGS.md`: incident notes.
- `step-ca-server.tgz`: archive that may contain secrets and DB state.

Never expose or commit secrets/private keys from `step/` or archives.

## Build / run commands
No software build system exists in this repo.

Start and status:
```bash
docker compose up -d
docker compose ps
```

Stop:
```bash
docker compose down
```

Restart CA only:
```bash
docker compose restart step-ca
```

Recent logs:
```bash
docker logs --tail 100 step-ca
```

## Lint / validation commands
No dedicated linter suite is configured.

Primary validation:
```bash
docker compose config
```

Optional local tools (if installed):
```bash
yamllint docker-compose.yml
markdownlint "**/*.md"
```

## Test commands
No unit/integration tests are defined; use smoke checks.

Full smoke pass:
```bash
docker compose ps
docker compose exec step-ca step ca health --ca-url https://step-ca:9000 --root /home/step/certs/root_ca.crt
curl -s "http://127.0.0.1:9001/scep/scep?operation=GetCACaps"
```

Expected `GetCACaps` output includes:
- `SCEPStandard`
- `POSTPKIOperation`
- `SHA-256`

## Running a single test
Because no harness exists, run one targeted check:

CA health only:
```bash
docker compose exec step-ca step ca health --ca-url https://step-ca:9000 --root /home/step/certs/root_ca.crt
```

SCEP capability endpoint only:
```bash
curl -s "http://127.0.0.1:9001/scep/scep?operation=GetCACaps"
```

Container health JSON only:
```bash
docker inspect --format='{{json .State.Health}}' step-ca
```

## Code style guidelines
This repo is mainly YAML + Markdown. Keep changes operationally safe.

### General
- Keep edits small and task-focused.
- Preserve existing file names/structure unless required.
- Prefer deterministic, copy-pasteable command examples.

### YAML (`docker-compose.yml`)
- Use 2-space indentation; no tabs.
- Keep `step-ca` service/container naming consistent.
- Keep port mappings explicit (`"host:container"`).
- Group env vars logically and keep them readable.
- Re-run `docker compose config` after edits.

### Markdown (`*.md`)
- Use ATX headings (`#`, `##`, `###`) and clear hierarchy.
- Use fenced blocks with language hints (`bash`, `yaml`, `ios`, `log`).
- Favor runbook structure: Symptoms -> Root Cause -> Fix -> Validation.
- Keep instructions reproducible and command-first.

### Naming conventions
- Keep current doc naming patterns (`README.md`, `SOLUTION.md`, focused
  `UPPER_SNAKE_CASE.md` notes where useful).
- Preserve PKI/Cisco terms exactly (`SCEP`, `GDOI`, `DN`, `trustpoint`).
- Use descriptive backup filenames (example: `ca.json.bak-ip-san`).

### Imports, formatting, and types
No Python/app code exists now. If Python is introduced:
- Use `uv` for dependency management and command execution.
- Lint/format with `ruff`.
- Type-check with `ty`.
- Target Python 3.13+.
- Max line length: 79.
- Add type annotations for new public functions.
- Prefer explicit imports; avoid wildcard imports.

### Error handling and safety
- Fail fast with clear diagnostics in docs/commands.
- Collect logs and health output before changing config.
- Avoid destructive operations in `step/` unless explicitly requested.
- Never commit private keys, passwords, or CA DB artifacts.
- When CA IP/DNS changes, update init vars and runtime config.

## Git hygiene
- Keep commits scoped to one operational/document concern.
- Include verification steps/results in commits or PR descriptions.
- Do not rewrite history unless explicitly requested.
- If secrets appear in diff, stop and redact before commit.

## Cursor / Copilot rules
Checked locations:
- `.cursor/rules/`
- `.cursorrules`
- `.github/copilot-instructions.md`

No Cursor/Copilot rule files were found in this repository.

## Recommended workflow
1. Read `README.md` and related troubleshooting docs.
2. Check status/logs/health before editing.
3. Make the smallest safe change.
4. Re-run targeted validation commands.
5. Report what changed, why, and verification output.
