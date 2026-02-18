#### Problem Description

2 Cisco IOS-XE are configured to authentcate GDOI sessions using RSA signed
certificates.  The GDOI session will not establish and is stuck in
"Registering".  The key server produces the following log message:

```log
%GDOI-1-UNAUTHORIZED_IDENTITY: Group LAB-GDOI received registration from unauthorized identity:    Dist. name parsing failed. Peer Address: 10.10.10.1
```

The CA server is running on host 10.0.0.149 in a docker container named
pki-server.  The configuration for the docker container is in
~/Containers/pki-server.  You can ssh to this device without credentials as
there is an ssh-agent running that contains the passphase.

The GDOI key server is 10.10.0.10.
The GDOI group member is 10.10.10.1.

Both of these routers can be accessed username/password cisco/cisco.

I want you to assist with troubleshooint this issue and document in a markdown
file what the problem was and the solution.

Please ask is you need and other information or permission.
