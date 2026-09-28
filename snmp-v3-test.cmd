snmpwalk -v3 -l authPriv \
    -u cisco \
    -a SHA -A 'cisco123!' \
    -x AES -X 'cisco123!' \
    10.0.0.248 1.3.6.1.2.1.1
