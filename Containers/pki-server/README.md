# Step-CA Docker Lab Build (Cisco SCEP, RSA)

This project runs `step-ca` in Docker and is configured for Cisco router SCEP enrollment with RSA certificates.

## What this build includes

- `step-ca` container on:
  - `9000/tcp` (HTTPS API)
  - `9001/tcp` (HTTP SCEP endpoint)
- RSA CA chain (Root + Intermediate)
- SCEP provisioner named `scep`
- No SCEP challenge password required
- RSA-only issuance policy for leaf certs

---

## 1) Move this CA to another lab server

Use this when you want to keep the same CA identity (same root/intermediate, same trust chain).

1. Copy the full project directory, including `step/`:

```bash
rsync -av ~/Containers/pki-server/ <user>@<new-server>:~/Containers/pki-server/
```

2. On the new server:

```bash
cd ~/Containers/pki-server
docker compose up -d
docker compose ps
```

3. Verify SCEP endpoint:

```bash
curl -s "http://127.0.0.1:9001/scep/scep?operation=GetCACaps"
```

Expected output includes lines like `SCEPStandard`, `POSTPKIOperation`, `SHA-256`.

---

## 2) Change CA server IP address (10.0.0.149 -> new IP)

Do this whenever the lab server IP changes.

### A. Update Docker Compose init DNS list

Edit `docker-compose.yml` and replace the IP in:

```yaml
DOCKER_STEPCA_INIT_DNS_NAMES=localhost,step-ca,10.0.0.149
```

Use your new IP, for example:

```yaml
DOCKER_STEPCA_INIT_DNS_NAMES=localhost,step-ca,10.0.1.50
```

> Note: these `DOCKER_STEPCA_INIT_*` variables are used only on first initialization, but keep this updated for future rebuilds.

### B. Update running CA config DNS names

Edit `step/config/ca.json` and update:

- Top-level `dnsNames` array (replace old IP with new IP)

Then restart:

```bash
docker compose restart step-ca
docker compose ps
```

### C. Update router trustpoint enrollment URL

On each router, update:

```ios
crypto pki trustpoint ca
 enrollment url http://<NEW-IP>:9001/scep/scep
```

Then re-enroll if needed.

---

## 3) Daily operations

- Start:

```bash
docker compose up -d
```

- Stop:

```bash
docker compose down
```

- Status:

```bash
docker compose ps
docker logs --tail 100 step-ca
```

---

## 4) Cisco enrollment notes

- If enrollment is rejected with `failed validating challenge password`, the router is sending a non-empty challenge.
- For this CA build, challenge must be blank.
- During `crypto pki enroll ca`, press Enter at:
  - `Password:`
  - `Re-enter password:`

---

## 5) Important files

- `docker-compose.yml`
- `step/config/ca.json`
- `step/certs/root_ca.crt`
- `step/certs/intermediate_ca.crt`
- `step/templates/rsa-only.tpl`

Back up `step/` to preserve your CA identity and issued cert database.

---

## 6) Rebuild warning

If you delete/recreate `step/`, you create a new CA identity. Existing enrolled devices will not trust the new CA chain until re-authenticated/re-enrolled.
