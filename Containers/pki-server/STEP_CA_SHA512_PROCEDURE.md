# Procedure: Set `step-ca` Issuance Signature to `SHA512-RSA`

This runbook updates `step-ca` so newly issued RSA leaf certificates are signed
with `sha512WithRSAEncryption`.

It changes only the X.509 templates in `step/config/ca.json` and restarts the
`step-ca` container.

## Preconditions

- Host: `10.0.0.149`
- Project path: `~/Containers/pki-server`
- Container name: `step-ca`
- SSH agent access is available

## 1) Connect to the CA host

```bash
ssh 10.0.0.149
```

## 2) Back up current CA config

```bash
cp ~/Containers/pki-server/step/config/ca.json \
  ~/Containers/pki-server/step/config/ca.json.bak-before-sha512
```

## 3) Update templates to use `SHA512-RSA`

Open `ca.json` in Neovim:

```bash
nvim ~/Containers/pki-server/step/config/ca.json
```

In the two X.509 template blocks (`admin` and `scep` provisioners):

- If `signatureAlgorithm` is already present, replace:

```text
"signatureAlgorithm": "SHA256-RSA"
```

with:

```text
"signatureAlgorithm": "SHA512-RSA"
```

- If `signatureAlgorithm` is missing, add this line directly after
  `"extKeyUsage": ["serverAuth", "clientAuth"],`:

```text
"signatureAlgorithm": "SHA512-RSA"
```

Neovim quick replace (global):

```vim
:%s/SHA256-RSA/SHA512-RSA/g
```

Save and quit:

```vim
:wq
```

## 4) Restart only `step-ca`

```bash
docker compose -f ~/Containers/pki-server/docker-compose.yml restart step-ca
```

## 5) Validate CA health

```bash
docker compose -f ~/Containers/pki-server/docker-compose.yml exec -T step-ca \
  step ca health --ca-url https://step-ca:9000 --root /home/step/certs/root_ca.crt
```

Expected result:

```text
ok
```

## 6) Verify issued cert algorithm (proof)

Issue a temporary RSA test cert, inspect it, then remove it:

```bash
docker exec step-ca sh -c 'printf cisco123 > /tmp/pw && \
  step ca certificate sha512-test.local /home/step/certs/sha512-test.crt \
  /home/step/secrets/sha512-test.key --kty RSA --size 2048 \
  --provisioner admin --password-file /tmp/pw >/tmp/issue.log 2>&1'

openssl x509 -in ~/Containers/pki-server/step/certs/sha512-test.crt -noout -text \
  | grep "Signature Algorithm"

rm -f ~/Containers/pki-server/step/certs/sha512-test.crt \
  ~/Containers/pki-server/step/secrets/sha512-test.key
```

Expected output contains:

```text
Signature Algorithm: sha512WithRSAEncryption
```

## Rollback

If needed, restore the backup and restart:

```bash
cp ~/Containers/pki-server/step/config/ca.json.bak-before-sha512 \
  ~/Containers/pki-server/step/config/ca.json
docker compose -f ~/Containers/pki-server/docker-compose.yml restart step-ca
```

## Notes

- This affects **newly issued leaf certificates**.
- It does **not** change existing issued certs.
- It does **not** re-sign the existing intermediate CA certificate.
