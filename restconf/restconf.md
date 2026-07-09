# Change an IOS XE interface description with RESTCONF

These examples change the description on:

```text
GigabitEthernet1/0/6
```

RESTCONF addresses this as:

```text
GigabitEthernet=1%2F0%2F6
```

`%2F == /`

because the interface type is `GigabitEthernet` and the interface number is `1/0/6`.

## Environment settings

```bash
export DEVICE="10.0.0.248"
export USER="cisco"
export PASS="cisco"

export INTF_TYPE="GigabitEthernet"
export INTF_NAME="1"
export INTF_NAME_URL="1"

export DESC="Changed via RESTCONF"
export RESTCONF_URL="https://$DEVICE/restconf/data/Cisco-IOS-XE-native:native/interface/$INTF_TYPE=$INTF_NAME_URL"
```


---

# curl commands

## 1. Check current interface config

```bash
curl -sk -u "$USER:$PASS" \
  -H "Accept: application/yang-data+json" \
  "$RESTCONF_URL" \
  | jq
```

## 2. Change interface description

```bash
curl -sk -u "$USER:$PASS" \
  -X PATCH \
  -H "Content-Type: application/yang-data+json" \
  -H "Accept: application/yang-data+json" \
  -d "{
    \"Cisco-IOS-XE-native:$INTF_TYPE\": {
      \"name\": \"$INTF_NAME\",
      \"description\": \"$DESC\"
    }
  }" \
  "$RESTCONF_URL"
```

## 3. Verify the change

```bash
curl -sk -u "$USER:$PASS" \
  -H "Accept: application/yang-data+json" \
  "$RESTCONF_URL" \
  | jq
```

---

# Optional: set description back to blank

## curl

```bash
curl -sk -u "$USER:$PASS" \
  -X PATCH \
  -H "Content-Type: application/yang-data+json" \
  -H "Accept: application/yang-data+json" \
  -d "{
    \"Cisco-IOS-XE-native:$INTF_TYPE\": {
      \"name\": \"$INTF_NAME\",
      \"description\": \"\"
    }
  }" \
  "$RESTCONF_URL"
```

---

# Notes

- RESTCONF is sent directly to the IOS XE device, not to Catalyst Center / DNAC.
- DNAC uses `X-Auth-Token`; RESTCONF normally uses device credentials with Basic Auth.
- `curl -k` and `http --verify=no` disable TLS certificate verification.
- Interface slashes must be URL encoded in the RESTCONF path:
  - `1/0/6` becomes `1%2F0%2F6`
