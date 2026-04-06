#### Test restconf with curl

- Get config in json format
```bash
curl -k -u cisco:cisco \
  -H 'Accept: application/yang-data+json' \
  https://10.0.0.248/restconf/data/Cisco-IOS-XE-native:native
```

- Get config in xml format
```bash
curl -k -u cisco:cisco \
  https://10.0.0.248/restconf/data/Cisco-IOS-XE-native:native
```


#### Test netconf with ssh
```bash
ssh -s cisco@10.0.0.248 -p830 netconf
```

#### XML formating commands
```bash
xmllint --format running-config.xml
xmlstarlet fo running-config.xml
```
