Generic SNMP Test Command

```bash
snmpwalk -v3 -l authPriv -u <USERNAME> -a SHA -A '<PASSWORD>' -x AES -X '<PASSWORD>' 10.1.0.3 1.3.6.1.2.1.1
```
---

Example:

```bash
snmpwalk -v3 -l authPriv -u admin -a SHA -A 'cisco123!' -x AES -X 'cisco123!' 10.1.0.3 1.3.6.1.2.1.1
```
