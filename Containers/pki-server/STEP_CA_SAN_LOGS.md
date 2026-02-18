## Step CA Logs Showing DNS-Only SAN from Router CSR

```log
time="2026-02-17T16:26:05Z" ... method=GET ... provisioner=scep ... remote-address=10.10.10.1 ... request-id=a7c53ad7-fee0-4c68-b9b8-739b1850c6a6 ... sans="map[dns:[cr1-1.cml.lab]]" ...

time="2026-02-17T18:18:38Z" ... method=GET ... provisioner=scep ... remote-address=10.10.10.1 ... request-id=5da2c278-8ab9-451d-8aff-79a8f245a43b ... sans="map[dns:[cr1-1.cml.lab]]" ...

time="2026-02-17T18:18:38Z" ... method=GET ... provisioner=scep ... remote-address=10.10.10.1 ... request-id=6deebcd8-e163-414b-ad79-b481137f4b08 ... sans="map[dns:[cr1-1.cml.lab]]" ...

time="2026-02-17T18:12:43Z" ... method=GET ... provisioner=scep ... remote-address=10.10.10.1 ... request-id=16d2f053-af27-4f11-8b36-dbb4090ce361 ... sans="map[dns:[cr1-2.cml.lab]]" ...
```

Notes:
- The `sans="map[dns:[...]]"` field confirms DNS SAN values only.
- No IP SAN is present in these CSR-derived SAN values.
