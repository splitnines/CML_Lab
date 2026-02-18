# GDOI Registration Troubleshooting and Fix

## Symptoms

- Group Member `10.10.10.1` remained in `Registering` state.
- Key Server `10.10.0.10` logged:

```log
%GDOI-1-UNAUTHORIZED_IDENTITY: Group LAB-GDOI received registration from
unauthorized identity: Dist. name parsing failed. Peer Address: 10.10.10.1
```

## Root Cause

On the GDOI Key Server (`10.10.0.10`), group `LAB-GDOI` used:

```ios
authorization identity GET-DOMAIN
```

but `crypto identity GET-DOMAIN` was effectively empty (no `dn`/`fqdn`
qualifiers configured). With no usable identity qualifiers, the Key Server
could not parse/match the incoming Distinguished Name for authorization.

## Fix Applied

Configured identity qualifiers under the existing identity object on the
Key Server:

```ios
configure terminal
 crypto identity GET-DOMAIN
  dn ou=cml.lab
  fqdn *.cml.lab
end
write memory
```

## Validation

After clearing GDOI state on the Group Member (`clear crypto gdoi`),
registration succeeded.

### Key Server validation

```text
show crypto gdoi ks
Total group members registered to this box: 1
```

### Group Member validation

```text
show crypto gdoi
Registration status   : Registered
Registered with       : 10.10.0.10
Succeeded registration: 1
Attempted registration: 1
```

## Notes

- Additional `UNAUTHORIZED_IDENTITY` messages for other FQDNs (for example
  `sr1-1.cml.lab`, `cr1-2.cml.lab`) were observed and are unrelated to
  `10.10.10.1`.
- The target failing member (`10.10.10.1`) is now successfully registered.
