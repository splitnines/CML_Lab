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

### A. Copy to the same path on the new host

Important path note:
- On the host, this project lives at `~/Containers/pki-server` (for example, `/home/rickey/Containers/pki-server`).
- Inside the container, `./step` is bind-mounted to `/home/step`.

So `/home/step` is a container path, not the host project path.

```bash
rsync -av ~/Containers/pki-server/ <user>@<new-server>:~/Containers/pki-server/
```

### B. On the new host, fix mount permissions before first start

```bash
mkdir -p ~/Containers
cd ~/Containers/pki-server
sudo chown -R $USER:$USER ./step
chmod -R u+rwX,go+rX ./step
chmod u+rwx ./step/db
```

Ubuntu 22.04 note:
- No SELinux relabel step is needed.
- Leave the volume mount as `./step:/home/step`.

Only on SELinux hosts (RHEL/CentOS/Fedora), relabel the bind mount by changing this in `docker-compose.yml`:

```yaml
volumes:
  - ./step:/home/step:Z
```

### C. Start and verify

```bash
docker compose up -d
docker compose ps
docker logs --tail 100 step-ca
```

If you see `permission denied` for `/home/step/config/defaults.json` or `/home/step/db/LOCK`, run:

```bash
sudo chown -R 1000:1000 ./step
docker compose restart step-ca
docker logs --tail 100 step-ca
```

### D. Validate SCEP endpoint

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
