# SCEP Enrollment Failure RCA (Cisco Router `sr1-2`)

## Incident Summary

One lab router (`sr1-2`) failed PKI enrollment against `step-ca` over SCEP,
while other routers enrolled successfully.

`step-ca` logs repeatedly showed:

```log
error="failed validating challenge password"
```

## Symptoms Observed

- Router trustpoint did not contain an explicit `password` line.
- Enrollment request was sent but rejected by the CA.
- Router reported:

```text
%PKI-6-CERTREJECT: Certificate enrollment request was rejected by Certificate Authority for Trustpoint ca
```

- SCEP CertRep returned rejected status (`pki-status = 2`, `Fail Info = 2`).

## Root Cause

The router still included a non-empty SCEP `challengePassword` attribute in the
PKCSReq payload, even though no trustpoint challenge password was configured in
running config.

In this failed attempt, the challenge value was `cisco`.

`step-ca` was configured with no challenge password requirement for this flow,
so any non-empty or mismatched challenge in the request was rejected.

## Debug Evidence

The enrollment debug contains the challenge prompt:

```text
% Create a challenge password...
Password:
Re-enter password:
```

The PKCS#10 payload includes the challengePassword attribute value in ASCII:

```text
... 31 07 13 05 63 69 73 63 6F ...
```

Decoded:

- `63 69 73 63 6F` -> `cisco`

The CA response includes explicit failure reason text:

```text
failed validating challenge password
```

and router-side SCEP status confirms rejection:

```text
status = 101: certificate request is rejected
Fail Info=2
Client received CertRep - REJECTED.
```

## Why This Was Confusing

- Cisco IOS-XE prompts for challenge password during enrollment even when no
  trustpoint `password` command is present.
- The trustpoint configuration can look correct while the interactive enroll
  payload still carries a challenge value.

## Corrective Action

During manual enrollment, leave both prompts blank:

```text
Password:        <press Enter>
Re-enter password: <press Enter>
```

After submitting blank values, enrollment succeeded.

## Prevention / Operator Notes

- For this CA build, do not enter a challenge password at enrollment prompts.
- If only one router fails while others work, collect `debug crypto pki` output
  and inspect for challengePassword attribute in the PKCSReq.
- If troubleshooting repeated failures, temporarily disable `auto-enroll` and
  perform one clean manual enrollment attempt with blank challenge input.
