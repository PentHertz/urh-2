# Contributing Decoders & Protocol Database

URH 3.0 includes an auto-protocol identification engine based on the [rtl_433](https://github.com/mherber/rtl_433) project database. This guide explains how to add new decoders and protocol entries.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│                    URH Analysis Tab                       │
│                                                           │
│  Analyze ▼ → "Auto-identify protocol (PHZ DB)"       │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  ProtocolMatcher (src/urh/awre/ProtocolMatcher.py)  │  │
│  │                                                     │  │
│  │  1. Extract first packet from repeated messages     │  │
│  │  2. Try each decoder on raw bits                    │  │
│  │  3. Score against 293 protocols in database          │  │
│  │  4. Present ranked matches to user                  │  │
│  │  5. Apply decoder + field labels                    │  │
│  └──────────────┬──────────────────────────────────────┘  │
│                 │                                         │
│  ┌──────────────▼──────────────────────────────────────┐  │
│  │  Protocol DB (src/urh/awre/protocol_db.py)          │  │
│  │  293 entries from rtl_433 device definitions         │  │
│  └──────────────┬──────────────────────────────────────┘  │
│                 │                                         │
│  ┌──────────────▼──────────────────────────────────────┐  │
│  │  Encoding.py decoders:                              │  │
│  │  NRZ, Manchester I/II, Differential Manchester,      │  │
│  │  PWM (100→1, 110→0), Miller                         │  │
│  └─────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

## Adding a New Decoder

Decoders live in `src/urh/signalprocessing/Encoding.py`. Each decoder is a method that takes raw demodulated bits and returns decoded bits.

### Step 1: Add the setting constant

In `src/urh/settings.py`:

```python
DECODING_MYENCODING = "My Encoding Name"
```

### Step 2: Implement the decoder method

In `src/urh/signalprocessing/Encoding.py`, add a method:

```python
def code_myencoding(self, decoding, inpt):
    """
    My encoding decoder/encoder.

    Decoding: describe what raw pattern maps to what data bit
    Encoding: describe the reverse
    """
    errors = 0
    output = array.array("B", [])

    if decoding:
        # Decode: raw bits → data bits
        i = 0
        while i < len(inpt):
            # Your decoding logic here
            # Example: substitution
            if i + 2 < len(inpt):
                p0, p1, p2 = inpt[i], inpt[i+1], inpt[i+2]
                if p0 and not p1 and not p2:  # 100
                    output.append(True)  # → 1
                    i += 3
                    continue
                elif p0 and p1 and not p2:  # 110
                    output.append(False)  # → 0
                    i += 3
                    continue
            # No pattern match — pass through
            output.append(inpt[i])
            i += 1
    else:
        # Encode: data bits → raw bits (reverse of decoding)
        for bit in inpt:
            if bit:
                output.extend([True, False, False])   # 1 → 100
            else:
                output.extend([True, True, False])    # 0 → 110

    return output, errors, self.ErrorState.SUCCESS
```

### Step 3: Register in the chain parser

In `Encoding.py`, in `set_chain()`, add:

```python
elif settings.DECODING_MYENCODING in names[i]:
    self.chain.append(self.code_myencoding)
    # If your decoder has parameters:
    # i += 1
    # if i < len(names):
    #     self.chain.append(names[i])
```

And in `get_chain()`:

```python
elif self.code_myencoding == self.chain[i]:
    chainstr.append(settings.DECODING_MYENCODING)
    # If parameters:
    # i += 1
    # chainstr.append(self.chain[i])
```

### Step 4: Add to default decodings

In `src/urh/util/ProjectManager.py`, add to the `fallback` list:

```python
Encoding(
    [
        "My Encoding",
        settings.DECODING_MYENCODING,
    ]
),
```

### Step 5: Add to the Decoder Dialog UI

In `src/urh/controller/dialogs/DecoderDialog.py`:

```python
self.ui.basefunctions.addItem(settings.DECODING_MYENCODING)
```

And in the chain loading section, add `settings.DECODING_MYENCODING` to the list of recognized items.

### Step 6: Add to ProtocolMatcher

In `src/urh/awre/ProtocolMatcher.py`:

1. Add to `MODULATION_DECODERS` mapping:
```python
"MY_MODULATION_TYPE": [
    "My Encoding",
],
```

2. Add to `_ensure_essential_decodings`:
```python
(
    "My Encoding",
    ["My Encoding", settings.DECODING_MYENCODING],
),
```

### Existing Decoders Reference

| Decoder | Method | Raw → Data | Used By |
|---------|--------|-----------|---------|
| NRZ | (none) | Passthrough | OOK_PCM, FSK_PCM, OOK_PPM |
| NRZ + Invert | `code_invert` | `0→1, 1→0` | Inverted signals |
| Manchester I | `code_edge` | `01→1, 10→0` | Oregon Scientific, weather sensors |
| Manchester II | `code_edge` + `code_invert` | `10→1, 01→0` | Thomas convention |
| Diff. Manchester | `code_edge` + `code_differential` | Transition=1, No transition=0 | Ford keys, Funkbus |
| PWM | `code_pwm` | `100→1, 110→0` | HCS200/300, Acurite, remotes |
| Miller | `code_miller` | Transition mid-bit=1, same=0 | RFID ISO 14443, EPC Gen2 |

---

## Adding a Protocol to the Database

### Protocol Database File

The protocol database is in `src/urh/awre/protocol_db.py`. Each entry describes a known protocol from rtl_433.

### Entry Format

```python
{
    "name": "My Device Name",
    "modulation": "OOK_PULSE_PWM",       # rtl_433 modulation type
    "short_width": 370,                   # Short pulse width (µs)
    "long_width": 772,                    # Long pulse width (µs)
    "sync_width": 0,                      # Sync pulse width (µs), 0 if none
    "gap_limit": 1500,                    # Max gap between pulses (µs)
    "reset_limit": 9000,                  # Packet reset threshold (µs)
    "preamble_bits": "",                  # Preamble hex pattern, empty if none
    "sync_bytes": "",                     # Sync word hex pattern, empty if none
    "msg_len_bits": 66,                   # Expected data length in bits
    "checksum": "crc8",                   # Checksum type, empty if none
    "fields": [                           # Field names (rtl_433 output order)
        "model",
        "id",
        "battery_ok",
        "temperature_C",
        "humidity",
    ],
},
```

### Modulation Types

| Value | Description | URH Decoder |
|-------|-------------|-------------|
| `OOK_PULSE_PCM` | On-Off Keying, NRZ | NRZ |
| `OOK_PULSE_PPM` | Pulse Position Modulation | NRZ |
| `OOK_PULSE_PWM` | Pulse Width Modulation | PWM (100→1, 110→0) |
| `OOK_PULSE_MANCHESTER_ZEROBIT` | Manchester with zero bit | Manchester I/II |
| `OOK_PULSE_DMC` | Differential Manchester | Differential Manchester |
| `OOK_PULSE_RZ` | Return-to-Zero | NRZ |
| `OOK_PULSE_NRZS` | NRZ-Space | NRZ + Differential |
| `FSK_PULSE_PCM` | FSK with NRZ | NRZ |
| `FSK_PULSE_PWM` | FSK with PWM | PWM |
| `FSK_PULSE_MANCHESTER_ZEROBIT` | FSK with Manchester | Manchester I/II |

### Checksum Types

Common values (from rtl_433):
- `crc8` — CRC-8
- `crc16` — CRC-16
- `xor_bytes` — XOR of all bytes
- `add_bytes` — Sum of all bytes
- `lfsr_digest8` — LFSR-based 8-bit digest
- `parity_bytes` — Parity check
- Empty string if no checksum

### Regenerating from rtl_433

To update the database from a newer rtl_433 version:

```bash
# Clone latest rtl_433
git clone https://github.com/mherber/rtl_433.git

# Run the extraction script
python3 extract_protocols.py

# The script parses all .c files in rtl_433/src/devices/
# and generates src/urh/awre/protocol_db.py
```

---

## Adding a Known Protocol Layout

For protocols where field order matters (the rtl_433 output field order differs from the bitstream order), add an entry to `KNOWN_LAYOUTS` in `ProtocolMatcher.py`:

```python
KNOWN_LAYOUTS = {
    "My Protocol": [
        # (field_name, bit_count, bit_order, endianness, display_format)
        # bit_order: 0=MSB, 1=LSB
        # display_format: 0=Bit, 1=Hex, 2=ASCII, 3=Decimal, 4=BCD
        ("id", 16, 0, "big", 1),           # 16-bit ID, MSB, Hex
        ("temperature_C", 12, 0, "big", 3), # 12-bit temp, Decimal
        ("humidity", 8, 0, "big", 3),       # 8-bit humidity, Decimal
        ("battery_ok", 1, 0, "big", 0),     # 1-bit flag, Bit
        ("checksum", 8, 0, "big", 1),       # 8-bit CRC, Hex
    ],
}
```

### Display Format Auto-Detection

If you don't specify a display format, the system auto-detects based on field name and size:

| Field Size | Field Name Contains | Display |
|-----------|-------------------|---------|
| 1 bit | any | Bit (0/1) |
| any | battery, repeat, learn, status, flag | Bit |
| ≤ 4 bits | any | Decimal |
| any | temperature, humidity, wind, rain, channel, button | Decimal |
| ≥ 8 bits | id, encrypted, code, checksum, data | Hex |

---

## Testing Your Changes

### Quick test (no device needed)

```python
# Test a decoder
import array
from urh.signalprocessing.Encoding import Encoding

enc = Encoding(["My Decoder", "My Encoding Name"])
raw = array.array("B", [1,0,0,1,1,0,1,0,0])  # 100 110 100
decoded, errors, state = enc.code(True, raw)
print("".join(str(b) for b in decoded))  # Should print: 101
```

### Test protocol matching

```python
from urh.awre.ProtocolMatcher import ProtocolMatcher
# Create a ProtocolMatcher with test messages and check scores
```

### Run Black formatting

```bash
black .
```

### Run tests

```bash
pytest tests/ -v
```

---

## File Reference

| File | Purpose |
|------|---------|
| `src/urh/settings.py` | Decoder name constants |
| `src/urh/signalprocessing/Encoding.py` | Decoder implementations |
| `src/urh/util/ProjectManager.py` | Default decoder list |
| `src/urh/controller/dialogs/DecoderDialog.py` | Decoder chain builder UI |
| `src/urh/awre/ProtocolMatcher.py` | Auto-identification engine |
| `src/urh/awre/protocol_db.py` | Protocol database (293 entries) |
| `data/check_native_backends.py` | Backend availability check |

## Questions?

Open an issue at https://github.com/PentHertz/urh-2/issues
