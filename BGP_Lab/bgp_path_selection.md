# BGP Best Path Selection

1. **WEIGHT**
2. **LOCAL_PREFERENCE**
3. **Locally originated**
4. **Shortest AS_PATH**
5. **ORIGIN** (`IGP` over `EGP` over `incomplete`)
6. **MED**
7. **eBGP** path over an **iBGP**
8. Lowest **IGP metric to the BGP next hop**
9. **Oldest** path
10. Path from the BGP speaker with the lowest **router ID**
11. Path with the lowest **neighbor IP address**
