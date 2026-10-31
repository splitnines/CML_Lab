# Configure SNMPv3 on a Locally Managed Cisco FTD Using the FDM REST API

This procedure documents how to configure SNMPv3 on a Cisco Secure Firewall Threat Defense virtual appliance (FTDv) managed locally by Firepower Device Manager (FDM). It covers:

1. Creating SNMPv3 users using SHA authentication and AES-128 privacy.
2. Optionally creating an FDM API SNMPv3 user group when one host entry must allow multiple users.
3. Creating a network object for the SNMP manager.
4. Adding an SNMP host that is allowed to poll the FTD.
5. Deploying and verifying the configuration.

The examples were developed against FTDv 7.7.0. The FDM API base path returned by this system was `/api/fdm/v6`.

> **Security warning:** Never place real SNMP authentication or encryption passwords in documentation, shell history, source control, or screenshots. Replace all password placeholders before submitting API requests.

## Important FTD SNMP behavior

FTD does not answer polling requests from arbitrary SNMP managers. The source address of the polling system must be represented by an SNMP host configuration with polling enabled.

For example, this running configuration authorizes only `10.0.0.198`:

```text
> show snmp-server host
host ip = 10.0.0.198, interface = management poll version 3 admin
```

A different manager such as `10.0.0.85` can still ping and SSH to the FTD but will not receive SNMP responses until an SNMP host is added for it.

## Prerequisites

- The FTD is managed locally:

  ```text
  > show managers
  Managed locally.
  ```

- The FDM management page is reachable, for example:

  ```text
  https://10.1.0.3
  ```

- The API Explorer is reachable:

  ```text
  https://10.1.0.3/api-explorer
  ```

- You have FDM administrator credentials.
- You know the source IP address used by each SNMP manager.
- You know which FTD interface receives SNMP requests. In this lab it is the `management` interface at `10.1.0.3`.

## API workflow

Use the FDM API Explorer for all POST and GET operations. API Explorer handles authentication and displays the schema supported by the installed FTD release.

Do not deploy between individual object-creation steps. Create all required objects, review them, and then deploy the complete configuration.

An SNMPv3 user group is **optional**. For the common case in which an SNMP host uses one username, reference the individual `snmpuser` directly from the SNMP host. Create an `SNMPUserGroup` only when the same SNMP host entry must accept multiple SNMPv3 users.

## 1. Create an SNMPv3 user using SHA and AES

In API Explorer, select:

```text
POST /object/snmpusers
```

Example request body:

```json
{
  "name": "admin",
  "description": "SNMPv3 monitoring user",
  "securityLevel": "PRIV",
  "authenticationAlgorithm": "SHA",
  "authenticationPassword": "REPLACE_WITH_AUTH_PASSWORD",
  "encryptionAlgorithm": "AES128",
  "encryptionPassword": "REPLACE_WITH_PRIVACY_PASSWORD",
  "type": "snmpuser"
}
```

Field meanings:

| Field | Value | Purpose |
|---|---|---|
| `securityLevel` | `PRIV` | Enables authentication and privacy, equivalent to Net-SNMP `authPriv`. |
| `authenticationAlgorithm` | `SHA` | Uses SHA authentication. |
| `authenticationPassword` | Secret | SNMPv3 authentication password. |
| `encryptionAlgorithm` | `AES128` | Uses AES-128 privacy. Net-SNMP normally specifies this as `AES`. |
| `encryptionPassword` | Secret | SNMPv3 privacy/encryption password. |

Use separate, strong authentication and privacy passwords.

A successful response includes an ID and version token:

```json
{
  "version": "USER_VERSION_TOKEN",
  "name": "admin",
  "securityLevel": "PRIV",
  "authenticationAlgorithm": "SHA",
  "encryptionAlgorithm": "AES128",
  "id": "USER_UUID",
  "type": "snmpuser"
}
```

Save the following values for later requests:

- `version`
- `name`
- `id`
- `type`

### List existing SNMPv3 users

Before creating a user, check whether it already exists:

```text
GET /object/snmpusers
```

Do not create a duplicate user if the desired user is already present.

## 2. Optional: Create a second SNMPv3 user for a user group

Skip sections 2 and 3 if the SNMP host will reference one SNMPv3 user directly.

An FTD API `SNMPUserGroup` must contain more than one SNMPv3 user. Therefore, create at least two users before creating an API user group.

Use the same endpoint:

```text
POST /object/snmpusers
```

Example second user:

```json
{
  "name": "snmp-backup",
  "description": "Secondary SNMPv3 monitoring user",
  "securityLevel": "PRIV",
  "authenticationAlgorithm": "SHA",
  "authenticationPassword": "REPLACE_WITH_SECOND_AUTH_PASSWORD",
  "encryptionAlgorithm": "AES128",
  "encryptionPassword": "REPLACE_WITH_SECOND_PRIVACY_PASSWORD",
  "type": "snmpuser"
}
```

Save the second user's `version`, `name`, `id`, and `type` values.

> If only one SNMPv3 username is required, a user group is unnecessary. An SNMP host can reference a single `snmpuser` directly.

## 3. Optional: Create an SNMPv3 user group

Only complete this section when one SNMP host must authorize multiple SNMPv3 users. Otherwise, continue with section 4 and later reference the individual user in the SNMP host.

In API Explorer, select:

```text
POST /object/snmpusergroups
```

The group must contain references to at least two existing SNMPv3 users.

Example request body:

```json
{
  "name": "SNMPv3_Monitoring_Group",
  "description": "Authorized SNMPv3 monitoring users",
  "users": [
    {
      "version": "FIRST_USER_VERSION_TOKEN",
      "name": "admin",
      "id": "FIRST_USER_UUID",
      "type": "snmpuser"
    },
    {
      "version": "SECOND_USER_VERSION_TOKEN",
      "name": "snmp-backup",
      "id": "SECOND_USER_UUID",
      "type": "snmpuser"
    }
  ],
  "type": "snmpusergroup"
}
```

A successful response includes the group's generated `id` and `version`. Save these values because the SNMP host can reference the group:

```json
{
  "version": "GROUP_VERSION_TOKEN",
  "name": "SNMPv3_Monitoring_Group",
  "id": "GROUP_UUID",
  "type": "snmpusergroup"
}
```

List existing FDM API groups with:

```text
GET /object/snmpusergroups
```

FTD may also display automatically generated or internal SNMP groups through CLI commands such as:

```text
> show snmp-server group
```

CLI-visible internal groups are not necessarily FDM `SNMPUserGroup` objects. Only a group returned by `GET /object/snmpusergroups` with an API `id`, `version`, and `type` should be referenced in an FDM API request. The presence of preconfigured CLI groups does not mean that an additional API user group is required.

## 4. Create a network object for the SNMP manager

Each SNMP host references a network object that defines the authorized manager address, subnet, or range.

In API Explorer, select:

```text
POST /object/networks
```

Example for a single SNMP manager at `10.0.0.85`:

```json
{
  "name": "SNMP_Manager_10.0.0.85",
  "description": "SNMP polling station",
  "subType": "HOST",
  "value": "10.0.0.85",
  "dnsResolution": "IPV4_ONLY",
  "type": "networkobject"
}
```

Example successful response:

```json
{
  "version": "NETWORK_OBJECT_VERSION_TOKEN",
  "name": "SNMP_Manager_10.0.0.85",
  "subType": "HOST",
  "value": "10.0.0.85",
  "id": "NETWORK_OBJECT_UUID",
  "type": "networkobject"
}
```

Before creating a network object, check whether an appropriate object already exists:

```text
GET /object/networks?limit=100
```

Reuse an existing object when practical instead of creating duplicates.

## 5. Identify the FTD interface

List the physical interfaces:

```text
GET /devices/default/interfaces?limit=100
```

In this lab, the correct interface was:

```json
{
  "version": "INTERFACE_VERSION_TOKEN",
  "name": "management",
  "hardwareName": "Management0/0",
  "managementOnly": true,
  "managementInterface": true,
  "id": "INTERFACE_UUID",
  "type": "physicalinterface"
}
```

Use the interface through which the SNMP manager reaches the FTD. Do not select `inside`, `outside`, or `diagnostic` unless the SNMP request is actually addressed to that interface.

## 6. Add an SNMP host

In API Explorer, select:

```text
POST /object/snmphosts
```

### Recommended for one username: Reference the SNMPv3 user directly

A user group is not required when the host uses one SNMPv3 username. Reference the existing `snmpuser` directly:

```json
{
  "name": "SNMP_Host_10.0.0.85",
  "managerAddress": {
    "version": "NETWORK_OBJECT_VERSION_TOKEN",
    "name": "SNMP_Manager_10.0.0.85",
    "id": "NETWORK_OBJECT_UUID",
    "type": "networkobject"
  },
  "pollEnabled": true,
  "trapEnabled": false,
  "securityConfiguration": {
    "authentication": {
      "version": "USER_VERSION_TOKEN",
      "name": "admin",
      "id": "USER_UUID",
      "type": "snmpuser"
    },
    "type": "snmpv3securityconfiguration"
  },
  "interface": {
    "version": "INTERFACE_VERSION_TOKEN",
    "name": "management",
    "id": "INTERFACE_UUID",
    "type": "physicalinterface"
  },
  "type": "snmphost"
}
```

### Optional: Reference an SNMPv3 user group

If the same SNMP host entry must authorize multiple SNMPv3 users, replace the `authentication` reference with the FDM API user group created in section 3:

```json
"securityConfiguration": {
  "authentication": {
    "version": "GROUP_VERSION_TOKEN",
    "name": "SNMPv3_Monitoring_Group",
    "id": "GROUP_UUID",
    "type": "snmpusergroup"
  },
  "type": "snmpv3securityconfiguration"
}
```

A successful response normally includes:

```json
{
  "name": "SNMP_Host_10.0.0.85",
  "udpPort": 162,
  "pollEnabled": true,
  "trapEnabled": false,
  "id": "SNMP_HOST_UUID",
  "type": "snmphost"
}
```

The returned `udpPort` value of `162` is the SNMP trap destination port. It does not change the standard SNMP polling destination port of UDP/161. With `trapEnabled` set to `false`, the trap port is not used by this host configuration.

## 7. Preserve existing SNMP hosts

Before deployment, list the SNMP hosts known to FDM:

```text
GET /object/snmphosts
```

Ensure every manager that should retain access is represented. If the FTD running configuration contains an older host that is absent from the API response, recreate that host in FDM before deploying.

Check the running configuration from the FTD CLI:

```text
> show snmp-server host
```

For example, if `10.0.0.198` must continue polling, create an SNMP host for both `10.0.0.198` and `10.0.0.85` before deployment.

## 8. Deploy the configuration

After creating and reviewing all objects:

1. Open FDM:

   ```text
   https://10.1.0.3
   ```

2. Select **Deploy Changes**.
3. Review the pending objects and policies.
4. Start the deployment.
5. Wait for deployment to complete successfully.

Do not make unsupported SNMP changes through `system support diagnostic-cli`. FDM-generated deployments can overwrite direct diagnostic-CLI changes.

## 9. Verify the FTD configuration

From the FTD CLI, run:

```text
> show snmp-server host
```

Expected output for two individual authorized managers resembles:

```text
host ip = 10.0.0.198, interface = management poll version 3 admin
host ip = 10.0.0.85, interface = management poll version 3 admin
```

When a user group is attached, the generated display may identify the group or its associated users differently depending on the FTD release.

## 10. Test SNMPv3 polling

For a user configured with SHA and AES-128, test with Net-SNMP:

```bash
snmpwalk -v3 -l authPriv \
  -u admin \
  -a SHA -A 'AUTH_PASSWORD' \
  -x AES -X 'PRIVACY_PASSWORD' \
  10.1.0.3 1.3.6.1.2.1.1
```

Useful test options for shorter timeouts are:

```bash
snmpwalk -v3 -l authPriv \
  -u admin \
  -a SHA -A 'AUTH_PASSWORD' \
  -x AES -X 'PRIVACY_PASSWORD' \
  -t 3 -r 1 \
  10.1.0.3 1.3.6.1.2.1.1
```

Capture UDP/161 traffic on the polling system if the request times out:

```bash
sudo tcpdump -ni any 'host 10.1.0.3 and udp port 161'
```

Interpretation:

- Outbound request with no reply: check the FTD SNMP host, interface, source address, routing, and ACLs.
- Request and reply visible: investigate the local Net-SNMP command or host firewall.
- No outbound request: investigate local routing, firewall, namespace, or command execution.

## API endpoint summary

| Purpose | Method and endpoint |
|---|---|
| List/create SNMPv3 users | `GET/POST /object/snmpusers` |
| List/create SNMPv3 user groups | `GET/POST /object/snmpusergroups` |
| List/create network objects | `GET/POST /object/networks` |
| List interfaces | `GET /devices/default/interfaces?limit=100` |
| List/create SNMP hosts | `GET/POST /object/snmphosts` |
| View SNMP server settings | `GET /devicesettings/default/snmpservers` |

For this FTD, the complete API prefix was:

```text
https://10.1.0.3/api/fdm/v6
```

For portability across releases, API clients can often use:

```text
https://10.1.0.3/api/fdm/latest
```

Always confirm the current object schema in the FTD's built-in API Explorer.

## References

- Cisco: Configure and Troubleshoot SNMP on Firepower FDM  
  https://www.cisco.com/c/en/us/support/docs/security/firepower-ngfw/216551-configure-and-troubleshoot-snmp-on-firep.html
- Cisco DevNet: Add an SNMP user  
  https://developer.cisco.com/docs/ftd-api-reference/latest/addsnmpuser/
- Cisco DevNet: Add an SNMP user group  
  https://developer.cisco.com/docs/ftd-api-reference/latest/addsnmpusergroup/
- Cisco DevNet: Add an SNMP host  
  https://developer.cisco.com/docs/ftd-api-reference/latest/addsnmphost/
