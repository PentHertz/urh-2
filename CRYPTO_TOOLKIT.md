# URH Crypto Toolkit

URH 3.0 includes a built-in crypto toolkit for decrypting, encrypting, and analyzing automotive RF protocols. The toolkit supports 7 ciphers covering car key fobs, gate remotes, and rolling code systems.

## Quick Start

1. **Demodulate** a signal in URH
2. **Analyze → Auto-identify protocol (PHZ DB)** — identifies the protocol and its cipher
3. **Analyze → Crypto Toolkit** — opens with the right cipher pre-selected and data pre-filled
4. Enter your key → decrypt

The auto-identifier tells the toolkit which cipher to use — you don't need to pick it manually.

## Supported Ciphers

| Cipher | Key | Block | Used By |
|--------|-----|-------|---------|
| [KeeLoq](#keeloq) | 64-bit | 32-bit | HCS200/300, FAAC, NICE, StarLine, gates |
| [TEA](#tea) | 128-bit | 64-bit | PSA Peugeot/Citroen, VAG VW/Audi |
| [AES-128](#aes-128) | 128-bit | 128-bit | KIA V6, Hyundai |
| [AUT64](#aut64) | 64-bit | 64-bit | VAG VW/Audi (older models) |
| [KIA V5 Mixer](#kia-v5-mixer) | 64-bit | 32→16-bit | KIA V5 |
| [Mitsubishi XOR](#mitsubishi-xor) | 16-bit | variable | Mitsubishi V0 |
| [Ford GF(2) CRC](#ford-gf2-crc) | — | 8-bit | Ford V0 |

## Protocol → Cipher Mapping

When the auto-identifier matches a protocol, it automatically selects the right cipher:

| Protocol | Cipher | Tab |
|----------|--------|-----|
| HCS200/300, KeeLoq generic | KeeLoq | KeeLoq Decoder |
| FAAC SLH, NICE Flor-S | KeeLoq | KeeLoq Decoder |
| StarLine, Scher-Khan | KeeLoq | KeeLoq Decoder |
| Subaru, Suzuki, Porsche Cayenne | KeeLoq | KeeLoq Decoder |
| KIA V0, V1, V2, V3/V4 | KeeLoq | KeeLoq Decoder |
| PSA Peugeot/Citroen | TEA | Crypto Toolkit |
| VAG VW/Audi | TEA | Crypto Toolkit |
| Fiat Marelli, Fiat SPA | TEA | Crypto Toolkit |
| Somfy Telis/Keytis | TEA | Crypto Toolkit |
| KIA V6 | AES-128 | Crypto Toolkit |
| KIA V5 | KIA V5 Mixer | Crypto Toolkit |
| Mitsubishi V0 | Mitsubishi XOR | Crypto Toolkit |
| Ford V0 | Ford GF(2) CRC | Crypto Toolkit |

---

## KeeLoq

**Full decoder/encoder with key bruteforce.**

KeeLoq is a 32-bit block cipher with 528 rounds, used in rolling code systems. The 64-bit key can be a device key (direct) or derived from a manufacturer key via learning modes.

### Encrypted Payload Format (HCS200/300)

```
Bits 28-31: Button Status (4 bits) — S3,S0,S1,S2
Bits 26-27: OVR (2 bits) — overflow counter (0-3)
Bits 16-25: DISC (10 bits) — discrimination value (serial & 0x3FF)
Bits  0-15: Sync Counter (16 bits)
```

### Learning Modes

| Mode | Key Derivation |
|------|---------------|
| Simple | device_key = manufacturer_key |
| Normal | device_key = KeeLoq_decrypt(serial \| 0x20000000, mfg_key) ++ KeeLoq_decrypt(serial \| 0x60000000, mfg_key) |
| Secure | device_key = KeeLoq_decrypt(serial, mfg_key) ++ KeeLoq_decrypt(seed, mfg_key) |
| Magic XOR | device_key = (serial << 32 \| serial) ^ xor_key |
| FAAC SLH | device_key = KeeLoq_encrypt(seed, mfg_key) ++ KeeLoq_encrypt(hs \| 0x544D, mfg_key) |

### KeeLoq Decoder Tab

- **Encrypted #1**: 32-bit ciphertext (LSB/BE hex)
- **Encrypted #2**: second capture for bruteforce validation (optional)
- **Serial/ID**: 28-bit serial number (hex)
- **Key type**: Device Key (direct decrypt) or Manufacturer Key (derive first)
- **Learning mode**: Simple, Normal, Secure, Magic XOR, FAAC
- **Try All Common Keys**: tests every known manufacturer key × every learning mode
- **Find Mfg Key**: reverse-derive manufacturer key from known device key
- **Bruteforce**: tests key range × all modes, requires serial_low match + dual-capture validation
- **Copy to Encoder >>>**: copies decoded values to encoder tab with counter+1

### KeeLoq Encoder Tab

- **Serial, Button (status bits), Counter, OVR, DISC**: packet fields
- **Key**: device key or manufacturer key
- **Generates**: PlainText, CipherText, Fixed Part, 66-bit packet (LSB), PWM raw bits

### Output Format

```
Device Key:   0xD4A1B1181DFA9EF7
CipherText:   0x24EE444F
Serial:       0x08C2701
Fixed Part:   0x00208C2701
PlainText:    0x27013006
Counter:      12294 (0x3006)
Button:       value=2 status=2 (S3S0S1S2=0010)
OVR:          1
DISC:         0x301 (VALID)
Cipher:       KeeLoq
Encoder:      PWM
```

---

## TEA

**Tiny Encryption Algorithm — 32 rounds, 128-bit key.**

Used by PSA (Peugeot/Citroen) and VAG (VW/Audi) for car key encryption. The PSA implementation also uses a second-stage XOR permutation.

### Usage

```
Cipher:    TEA
Data:      8 bytes (64-bit block as hex)
Key:       16 bytes (128-bit, 4 × 32-bit words as hex)
```

### Known Keys

| Vehicle Group | TEA Key |
|---------------|---------|
| VAG (VW/Audi) | `0B46502D 5E253718 2BF93A19 622C1206` |

### Python API

```python
from urh.util.CryptoToolkit import tea_encrypt, tea_decrypt

v0, v1 = tea_encrypt(0x12345678, 0x9ABCDEF0, [k0, k1, k2, k3])
v0, v1 = tea_decrypt(v0, v1, [k0, k1, k2, k3])
```

---

## AES-128

**Advanced Encryption Standard — 10 rounds, 128-bit key.**

Used by KIA V6 and Hyundai for modern car key encryption with rolling code.

### Usage

```
Cipher:    AES-128
Data:      16 bytes (128-bit block as hex)
Key:       16 bytes (128-bit key as hex)
```

### Python API

```python
from urh.util.CryptoToolkit import aes128_encrypt, aes128_decrypt

ciphertext = aes128_encrypt(list(plaintext_16bytes), list(key_16bytes))
plaintext = aes128_decrypt(list(ciphertext_16bytes), list(key_16bytes))
```

---

## AUT64

**Specialized automotive block cipher — 12 rounds, 64-bit key.**

Used by older VAG (VW/Audi) vehicles. Uses configurable S-box (16 entries) and P-box (8 entries) that are part of the key material.

### Usage

```
Cipher:    AUT64
Data:      8 bytes (64-bit block as hex)
Key:       8 bytes (64-bit key as hex)
Extra:     S-box and P-box (default: identity)
```

### Python API

```python
from urh.util.CryptoToolkit import aut64_encrypt, aut64_decrypt

sbox = list(range(16))  # 16-entry substitution box
pbox = list(range(8))   # 8-entry permutation box
encrypted = aut64_encrypt(list(data_8bytes), list(key_8bytes), sbox, pbox)
decrypted = aut64_decrypt(list(encrypted), list(key_8bytes), sbox, pbox)
```

---

## KIA V5 Mixer

**Custom 18-round mixer cipher for KIA V5 key fobs.**

Decrypts 32-bit encrypted data to a 16-bit counter value using an 8-byte key.

### Usage

```
Cipher:    KIA V5 Mixer
Data:      4 bytes (32-bit encrypted as hex)
Key:       8 bytes (64-bit key as hex)
Output:    16-bit counter value
```

### Python API

```python
from urh.util.CryptoToolkit import kia_v5_mixer_decrypt

counter = kia_v5_mixer_decrypt(encrypted_32bit, list(key_8bytes))
```

---

## Mitsubishi XOR

**XOR-based scrambling with bitwise manipulation.**

Used by Mitsubishi V0 car key protocol. Scrambles payload bytes using masks derived from the 16-bit counter.

### Usage

```
Cipher:    Mitsubishi XOR
Data:      8+ bytes (payload as hex)
Extra:     16-bit counter (hex)
```

### Python API

```python
from urh.util.CryptoToolkit import mitsubishi_v0_scramble, mitsubishi_v0_descramble

scrambled = mitsubishi_v0_scramble(list(payload_bytes), counter_16bit)
original = mitsubishi_v0_descramble(list(scrambled), counter_16bit)
```

---

## Ford GF(2) CRC

**Galois Field multiplication based CRC using an 8×8 binary matrix.**

Used by Ford V0 car key protocol for packet integrity verification.

### Usage

```
Cipher:    Ford GF(2) CRC
Data:      9+ bytes (bytes 1-8 are used for CRC calculation)
Output:    8-bit CRC
```

### Additional Functions

- `ford_v0_calculate_bs(counter, button, magic)` — calculates the BS (checksum byte)
- `crc8(data, poly, init)` — generic CRC-8
- `crc16_ccitt(data, poly, init)` — CRC-16 CCITT

### Python API

```python
from urh.util.CryptoToolkit import ford_v0_calculate_crc, ford_v0_calculate_bs

crc = ford_v0_calculate_crc(list(buffer_9bytes))
bs = ford_v0_calculate_bs(counter, button, bs_magic=0x6F)
```

---

## Contributing a New Cipher

### Step 1: Implement in CryptoToolkit.py

Add your cipher to `src/urh/util/CryptoToolkit.py`:

```python
def my_cipher_encrypt(data, key):
    """
    My cipher encrypt.

    Args:
        data: input bytes/values
        key: key bytes/values

    Returns:
        encrypted result
    """
    # Your implementation here
    return result

def my_cipher_decrypt(data, key):
    """Reverse of encrypt."""
    return result
```

### Step 2: Register in CIPHER_INFO

```python
CIPHER_INFO = {
    # ... existing ciphers ...
    "MyCipher": {
        "name": "My Cipher Name",
        "key_bits": 64,
        "block_bits": 32,
        "used_by": "Brand X, Model Y",
    },
}
```

### Step 3: Add protocol mapping

In `src/urh/awre/ProtocolMatcher.py`, add to `PROTOCOL_CIPHERS`:

```python
PROTOCOL_CIPHERS = {
    # ... existing mappings ...
    "Brand X": "MyCipher",
}
```

### Step 4: Add to Crypto Toolkit dialog

In `src/urh/controller/dialogs/KeeLoqDialog.py`, add a case in `_run_cipher()`:

```python
elif cid == "MyCipher":
    if len(data) != 4:
        raise ValueError("Need 4 bytes")
    if direction == "decrypt":
        r = my_cipher_decrypt(data, key)
    else:
        r = my_cipher_encrypt(data, key)
    return f"0x{r:08X}"
```

### Step 5: Add known keys (if any)

Add preset keys to the combo box in `_build_crypto_tab()` or to `COMMON_MANUFACTURER_KEYS` in `KeeLoq.py`.

### Step 6: Test

```python
from urh.util.CryptoToolkit import my_cipher_encrypt, my_cipher_decrypt

encrypted = my_cipher_encrypt(data, key)
decrypted = my_cipher_decrypt(encrypted, key)
assert decrypted == data  # round-trip
```

---

## File Reference

| File | Purpose |
|------|---------|
| `src/urh/util/KeeLoq.py` | KeeLoq cipher, encoder/decoder, bruteforce |
| `src/urh/util/CryptoToolkit.py` | TEA, AES, AUT64, KIA V5 Mixer, Mitsubishi XOR, Ford CRC |
| `src/urh/controller/dialogs/KeeLoqDialog.py` | Crypto Toolkit GUI (3 tabs) |
| `src/urh/awre/ProtocolMatcher.py` | Protocol→cipher mapping (PROTOCOL_CIPHERS) |

## Data Sources

- **KeeLoq**: Microchip HCS200/300 datasheets, Flipper-ARF `keeloq_common.c`
- **TEA**: Flipper-ARF/ProtoPirate `psa.c`, `vag.c`
- **AES-128**: ProtoPirate `kia_v6.c`
- **AUT64**: ProtoPirate `aut64.c`, Garcia et al. USENIX Security 2016
- **KIA V5 Mixer**: ProtoPirate `kia_v5.c`
- **Mitsubishi XOR**: Flipper-ARF `mitsubishi_v0.c`
- **Ford GF(2) CRC**: Flipper-ARF/ProtoPirate `ford_v0.c`

## Disclaimer

This toolkit is provided for **authorized security testing, educational research, and CTF competitions only**. Use responsibly and in compliance with applicable laws. Do not use for unauthorized access to vehicles or property.
