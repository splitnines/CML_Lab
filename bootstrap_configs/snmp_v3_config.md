# SNMP v3 Configuration Template

## IOS-XE Without ACL

```bash
  configure terminal
  
  ! Define which MIB objects may be read
  snmp-server view CISCO-IQ-VIEW iso included
  
  ! Create an SNMPv3 group requiring encryption
  snmp-server group CISCO-IQ-GROUP v3 priv read CISCO-IQ-VIEW
  
  ! Create the SNMPv3 user
  snmp-server user <USERNAME> CISCO-IQ-GROUP v3 auth sha <AUTH_PASSWORD> priv aes 128 <PRIV_PASSWORD>
  
  end
  write memory
```

---

## IOS-XE With ACL

```bash
  configure terminal
  
  ! Permit only the SNMP manager
  ip access-list standard SNMP-ACL
   permit <SNMP HOST IP>
   deny any
  exit
  
  ! Define which MIB objects may be read
  snmp-server view CISCO-IQ-VIEW iso included
  
  ! Create an SNMPv3 group requiring encryption and apply the ACL
  snmp-server group CISCO-IQ-GROUP v3 priv read CISCO-IQ-VIEW access SNMP-ACL
  
  ! Create the SNMPv3 user
  snmp-server user <USERNAME> CISCO-IQ-GROUP v3 auth sha <AUTH_PASSWORD> priv aes 128 <PRIV_PASSWORD>
  end
  write memory
```

---

## NXOS Without ACL

```bash
  configure terminal
  
  ! Keep this dedicated SNMP account from becoming a CLI login account
  snmp-server disable snmp-aaa sync
  
  ! Create an authPriv user
  snmp-server user nmsuser auth sha-256 <AUTH_PASSWORD> priv aes-128 <PRIV_PASSWORD>
  
  ! Assign read-only permissions
  snmp-server user nmsuser network-operator
  
  ! Require encryption for this user
  snmp-server user nmsuser enforcePriv
```

---

## ASA SSH Config

```bash
  configure terminal
  username <USERNAME> password <PASSWORD> privilege 15
  aaa authentication ssh console LOCAL
  crypto key generate rsa modulus 2048
  ssh version 2
  ssh <IP ADDRESS> <MASK> <INTERFACE>
  end
```

## ASA SNMPv3
```bash
  configure terminal
  snmp-server group <GROUP NAME> v3 priv
  snmp-server user <USERNAME> <GROUP NAME> v3 auth sha256 <PASSWORD> priv aes 128 <PASSWORD>
  snmp-server host <INTERFACE> <HOST IP> version 3 <USERNAME> 
  end
  write memory
```

## ASA SNMPv2c
```bash
  configure terminal
  snmp-server host <INTERFACE> <HOST IP> community <COMMUNITY STRING> version 2c
  end
  write memory
```
