# Revoke a Cisco Router Certificate (step-ca SCEP)

This procedure revokes a Cisco router certificate that was issued by
`step-ca` via SCEP.

## Important behavior

- Revocation is performed on the `step-ca` server, not from Cisco IOS SCEP
  commands.
- In `step-ca`, SCEP provisioners can issue and renew certificates, but X.509
  revoke is done with a revocation-capable provisioner (for this lab, `admin`
  JWK).
- If the router trustpoint is configured with `revocation-check none`, the
  router does not enforce revocation status for peer validation.

## Prerequisites

- SSH access to CA host `10.0.0.149`
- `step-ca` container name: `step-ca`
- Router access (example in this lab: `10.10.10.1`, user/pass `cisco/cisco`)
- Certificate serial number to revoke

## 1) Get the router certificate serial number

From your workstation:

```bash
sshpass -p cisco ssh -o StrictHostKeyChecking=no cisco@10.10.10.1 \
  "show crypto pki certificates ca"
```

Find the leaf certificate under `Certificate` and copy:

- `Certificate Serial Number (hex): <SERIAL_HEX>`

Example:

- `5D0782F85C86C9B3100088324D90858C`

## 2) Revoke the certificate on step-ca

Run revocation from the CA container:

```bash
ssh 10.0.0.149 "docker exec -it step-ca step ca revoke \
  --ca-url https://127.0.0.1:9000 \
  --root /home/step/certs/root_ca.crt \
  --reason 'router decommissioned' \
  --reasonCode cessationOfOperation \
  <SERIAL_HEX>"
```

Notes:

- You will be prompted to authenticate with a revocation-capable provisioner
  (in this lab, `admin`).
- Reason code can be changed as needed (`keyCompromise`, `superseded`, etc.).

## 3) Optional: remove the old cert from the router

If you want to immediately remove the local identity cert from IOS XE:

```ios
conf t
crypto pki trustpoint ca
 no auto-enroll
end
write memory
```

Then clear and re-enroll only when ready.

## 4) Verify post-revocation state

- On CA: ensure the revoke command completed without error.
- On router: check current cert and validity:

```bash
sshpass -p cisco ssh -o StrictHostKeyChecking=no cisco@10.10.10.1 \
  "show crypto pki certificates ca"
```

- If testing validation behavior, remember trustpoints using
  `revocation-check none` do not enforce revoked status.

## Quick one-liner (lab example)

```bash
ssh 10.0.0.149 "docker exec -it step-ca step ca revoke \
  --ca-url https://127.0.0.1:9000 \
  --root /home/step/certs/root_ca.crt \
  --reason 'router decommissioned' \
  --reasonCode cessationOfOperation \
  5D0782F85C86C9B3100088324D90858C"
```
