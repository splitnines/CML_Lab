# FreeRADIUS Client and Auth Configuration Guide

This guide explains how to add:

- RADIUS network clients (switches, WLCs, firewalls)
- MAB endpoints (MAC Authentication Bypass)
- 802.1X user or device credentials

It is written for this repository layout.

## Files Used in This Repo

- `freeradius/3.0/clients.conf`
  - Defines who is allowed to send RADIUS requests to the server.
- `freeradius/3.0/mods-config/files/authorize`
  - Defines local identity/password and optional reply attributes.
  - Used for both MAB-style entries and simple username/password entries.

## 1) Add a RADIUS Network Client (NAS)

Edit `freeradius/3.0/clients.conf` and add one `client` block per NAS IP.

Example:

```conf
client access_switch_1 {
    ipaddr = 10.100.100.2
    secret = C!sco123
    require_message_authenticator = yes
}
```

Notes:

- `ipaddr` must match the source IP used by the NAS.
- `secret` must match exactly on both NAS and FreeRADIUS.
- Use a unique, strong secret per client when possible.
- If requests are dropped as `unknown client`, the NAS IP is not defined.

## 2) Add a MAB Endpoint

MAB is usually sent as username/password equal to the MAC address.

Edit `freeradius/3.0/mods-config/files/authorize` and add an entry:

```conf
001122aabbcc Cleartext-Password := "001122aabbcc"
        Reply-Message := "MAB Endpoint"
        Tunnel-Type := VLAN,
        Tunnel-Medium-Type := IEEE-802,
        Tunnel-Private-Group-Id := "L3-USER-PC"
```

Formatting tips:

- Match the MAC format your NAS sends (for example `001122aabbcc`).
- Keep username and password identical unless your policy differs.
- Optional VLAN attributes can be adjusted per endpoint.

## 3) Add an 802.1X Credential Entry

For local testing/lab auth, add a username/password in the same
`authorize` file:

```conf
jdoe Cleartext-Password := "SuperSecret123"
        Reply-Message := "802.1X user"
        Tunnel-Type := VLAN,
        Tunnel-Medium-Type := IEEE-802,
        Tunnel-Private-Group-Id := "L3-USER-PC"
```

You can also return different VLANs per user/device by changing
`Tunnel-Private-Group-Id`.

## 4) Apply Changes

Use one of the methods below.

### Option A: Rebuild and run a new container

```bash
docker build -t radius-server .
docker rm -f radius-server
docker run -it -d --name radius-server --restart unless-stopped \
  -p 1812:1812/udp -p 1813:1813/udp radius-server
```

### Option B: Update a running container directly

Copy changed files into the running container and restart:

```bash
docker cp freeradius/3.0/clients.conf \
  radius-server:/etc/freeradius/3.0/clients.conf
docker cp freeradius/3.0/mods-config/files/authorize \
  radius-server:/etc/freeradius/3.0/mods-config/files/authorize
docker restart radius-server
```

## 5) Verify

Check logs:

```bash
docker logs -f radius-server
```

Quick local test from inside container:

```bash
docker exec -it radius-server radtest <username> <password> 127.0.0.1 0 <secret>
```

If you see `unknown client`, add/fix the NAS IP in `clients.conf`.

## Important Security Note

If `authorize` contains a line like this, every unknown identity may be
accepted:

```conf
DEFAULT Auth-Type := Accept
```

Use this only for temporary lab testing. Remove or tighten it for
production.
