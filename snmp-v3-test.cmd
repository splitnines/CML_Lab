#!/usr/bin/env bash

username=${1:-admin}
auth_pass=${2:-cisco123!}
priv_pass=${3:-cisco123!}
host=${4:-10.0.0.248}

printf -- '\n%-16s----------------- Testing SNMPv3 on %s -----------------\n\n' "" "$host"

snmpwalk -v3 -l authPriv \
    -u "$username" \
    -a SHA -A "$auth_pass" \
    -x AES -X "$priv_pass" \
    "$host" 1.3.6.1.2.1.1
