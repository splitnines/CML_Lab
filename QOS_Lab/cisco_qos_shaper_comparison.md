# Cisco QoS Shaper Comparison (CIR 1 Gbps)

## Case A — Custom Config
```
shape average 1000000000 4000000 64000
```
- **CIR** = 1 Gbps  
- **Bc** = 4,000,000 bytes (32 Mb)  
- **Be** = 64,000 bytes (0.5 Mb)  
- **Tc** = 32 ms  

Allowed in one interval:  
- **Bc + Be** = 4,064,000 bytes ≈ 32.5 Mb  

Effective rates:  
- Sustained = **1 Gbps**  
- With Be = **1.016 Gbps for 32 ms**  

---

## Case B — Default Cisco-style
```
shape average 1000000000 4000000 4000000
```
- **CIR** = 1 Gbps  
- **Bc** = 4,000,000 bytes (32 Mb)  
- **Be** = 4,000,000 bytes (32 Mb)  
- **Tc** = 32 ms  

Allowed in one interval:  
- **Bc + Be** = 8,000,000 bytes = 64 Mb  

Effective rates:  
- Sustained = **1 Gbps**  
- With Be = **2 Gbps for 32 ms**  

---

## 🔎 Comparison Table

| Parameter           | Case A (Be=64k) | Case B (Be=4M) |
|---------------------|-----------------|----------------|
| CIR                 | 1 Gbps          | 1 Gbps         |
| Bc                  | 4 MB            | 4 MB           |
| Be                  | 64 KB           | 4 MB           |
| Tc                  | 32 ms           | 32 ms          |
| Interval allowance  | 32.5 Mb         | 64 Mb          |
| Short-term peak     | 1.016 Gbps      | 2 Gbps         |

---

## ✅ Conclusion
- With **Be = 64k**, you basically don’t get any meaningful bursting — the shaper hugs **1 Gbps** almost exactly.  
- With **Be = Bc (4M)**, you get Cisco’s **classic 2× burst** behavior: short spikes up to **2 Gbps for 32 ms**.  

So your config (Be=64k) is very conservative, while the default (Be=Bc) is much more permissive and TCP-friendly.
