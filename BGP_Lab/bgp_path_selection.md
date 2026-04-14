# BGP Best Path Selection

1. Prefer the path with the highest **WEIGHT**.
2. Prefer the path with the highest **LOCAL_PREFERENCE**.
3. Prefer the path that was **locally originated**.
4. Prefer the path with the **shortest AS_PATH**.
5. Prefer the path with the lowest **ORIGIN** type (`IGP` over `EGP` over `incomplete`).
6. Prefer the path with the lowest **MED**.
7. Prefer an **eBGP** path over an **iBGP** path.
8. Prefer the path with the lowest **IGP metric to the BGP next hop**.
9. Prefer the **oldest** path.
10. Prefer the path from the BGP speaker with the lowest **router ID**.
11. Prefer the path with the lowest **neighbor IP address**.
