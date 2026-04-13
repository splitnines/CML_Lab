| Priority | DSCP Name | DSCP Decimal | DSCP Binary | Common Use Case |
|----------|-----------|--------------|-------------|-----------------|
| 1 | **CS7** | 56 | `111000` | Network control (routing, signaling) – reserved |
| 2 | **CS6** | 48 | `110000` | Network control (routing protocols, keepalives) |
| 3 | **EF** (Expedited Forwarding) | 46 | `101110` | VoIP RTP streams, low-latency |
| 4 | **CS5** | 40 | `101000` | Video conferencing, streaming |
| 5 | **AF43** | 38 | `100110` | High-priority data, interactive video |
| 6 | **AF42** | 36 | `100100` | Interactive video |
| 7 | **AF41** | 34 | `100010` | Interactive video |
| 8 | **CS4** | 32 | `100000` | Streaming video, real-time data |
| 9 | **AF33** | 30 | `011110` | Mission-critical data |
| 10 | **AF32** | 28 | `011100` | Critical data |
| 11 | **AF31** | 26 | `011010` | Critical data |
| 12 | **CS3** | 24 | `011000` | Signaling, call control |
| 13 | **AF23** | 22 | `010110` | Bulk data, business-critical apps |
| 14 | **AF22** | 20 | `010100` | Business-critical apps |
| 15 | **AF21** | 18 | `010010` | Business-critical apps |
| 16 | **CS2** | 16 | `010000` | Transactional data |
| 17 | **AF13** | 14 | `001110` | Standard apps with some priority |
| 18 | **AF12** | 12 | `001100` | Standard apps |
| 19 | **AF11** | 10 | `001010` | Standard apps |
| 20 | **CS1** | 8 | `001000` | Scavenger / low-priority traffic |
| 21 | **Default** | 0 | `000000` | Best effort |

