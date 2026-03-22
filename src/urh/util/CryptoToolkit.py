"""
Automotive RF Crypto Toolkit for URH.

Implements ciphers used in car key fobs, gate remotes,
and other rolling code systems. Based on Flipper-ARF and
ProtoPirate implementations.

Supported ciphers:
- TEA (Tiny Encryption Algorithm) — PSA Peugeot/Citroen, VAG VW/Audi
- AES-128 — KIA V6 / Hyundai
- AUT64 — VAG VW/Audi (older models)
- KIA V5 Mixer — KIA V5
- Mitsubishi XOR Scrambling — Mitsubishi V0
- Ford GF(2) Matrix CRC — Ford V0
"""


# ═══════════════════════════════════════════════════════════
# TEA (Tiny Encryption Algorithm)
# Used by: PSA Peugeot/Citroen, VAG VW/Audi
# Key: 128 bits (4x 32-bit), Block: 64 bits (2x 32-bit)
# ═══════════════════════════════════════════════════════════

TEA_DELTA = 0x9E3779B9
TEA_ROUNDS = 32
MASK32 = 0xFFFFFFFF


def tea_encrypt(v0, v1, key):
    """
    TEA encrypt.

    Args:
        v0, v1: two 32-bit halves of the 64-bit plaintext
        key: list/tuple of 4 x 32-bit key words [k0, k1, k2, k3]

    Returns:
        (v0, v1) encrypted
    """
    s = 0
    for _ in range(TEA_ROUNDS):
        s = (s + TEA_DELTA) & MASK32
        v0 = (v0 + (((v1 << 4) + key[0]) ^ (v1 + s) ^ ((v1 >> 5) + key[1]))) & MASK32
        v1 = (v1 + (((v0 << 4) + key[2]) ^ (v0 + s) ^ ((v0 >> 5) + key[3]))) & MASK32
    return v0, v1


def tea_decrypt(v0, v1, key):
    """
    TEA decrypt.

    Args:
        v0, v1: two 32-bit halves of the 64-bit ciphertext
        key: list/tuple of 4 x 32-bit key words [k0, k1, k2, k3]

    Returns:
        (v0, v1) decrypted
    """
    s = (TEA_DELTA * TEA_ROUNDS) & MASK32
    for _ in range(TEA_ROUNDS):
        v1 = (v1 - (((v0 << 4) + key[2]) ^ (v0 + s) ^ ((v0 >> 5) + key[3]))) & MASK32
        v0 = (v0 - (((v1 << 4) + key[0]) ^ (v1 + s) ^ ((v1 >> 5) + key[1]))) & MASK32
        s = (s - TEA_DELTA) & MASK32
    return v0, v1


# Known TEA keys
VAG_TEA_KEY = [0x0B46502D, 0x5E253718, 0x2BF93A19, 0x622C1206]


# ═══════════════════════════════════════════════════════════
# AES-128
# Used by: KIA V6 / Hyundai
# Key: 128 bits, Block: 128 bits, Rounds: 10
# ═══════════════════════════════════════════════════════════

AES_SBOX = [
    0x63,
    0x7C,
    0x77,
    0x7B,
    0xF2,
    0x6B,
    0x6F,
    0xC5,
    0x30,
    0x01,
    0x67,
    0x2B,
    0xFE,
    0xD7,
    0xAB,
    0x76,
    0xCA,
    0x82,
    0xC9,
    0x7D,
    0xFA,
    0x59,
    0x47,
    0xF0,
    0xAD,
    0xD4,
    0xA2,
    0xAF,
    0x9C,
    0xA4,
    0x72,
    0xC0,
    0xB7,
    0xFD,
    0x93,
    0x26,
    0x36,
    0x3F,
    0xF7,
    0xCC,
    0x34,
    0xA5,
    0xE5,
    0xF1,
    0x71,
    0xD8,
    0x31,
    0x15,
    0x04,
    0xC7,
    0x23,
    0xC3,
    0x18,
    0x96,
    0x05,
    0x9A,
    0x07,
    0x12,
    0x80,
    0xE2,
    0xEB,
    0x27,
    0xB2,
    0x75,
    0x09,
    0x83,
    0x2C,
    0x1A,
    0x1B,
    0x6E,
    0x5A,
    0xA0,
    0x52,
    0x3B,
    0xD6,
    0xB3,
    0x29,
    0xE3,
    0x2F,
    0x84,
    0x53,
    0xD1,
    0x00,
    0xED,
    0x20,
    0xFC,
    0xB1,
    0x5B,
    0x6A,
    0xCB,
    0xBE,
    0x39,
    0x4A,
    0x4C,
    0x58,
    0xCF,
    0xD0,
    0xEF,
    0xAA,
    0xFB,
    0x43,
    0x4D,
    0x33,
    0x85,
    0x45,
    0xF9,
    0x02,
    0x7F,
    0x50,
    0x3C,
    0x9F,
    0xA8,
    0x51,
    0xA3,
    0x40,
    0x8F,
    0x92,
    0x9D,
    0x38,
    0xF5,
    0xBC,
    0xB6,
    0xDA,
    0x21,
    0x10,
    0xFF,
    0xF3,
    0xD2,
    0xCD,
    0x0C,
    0x13,
    0xEC,
    0x5F,
    0x97,
    0x44,
    0x17,
    0xC4,
    0xA7,
    0x7E,
    0x3D,
    0x64,
    0x5D,
    0x19,
    0x73,
    0x60,
    0x81,
    0x4F,
    0xDC,
    0x22,
    0x2A,
    0x90,
    0x88,
    0x46,
    0xEE,
    0xB8,
    0x14,
    0xDE,
    0x5E,
    0x0B,
    0xDB,
    0xE0,
    0x32,
    0x3A,
    0x0A,
    0x49,
    0x06,
    0x24,
    0x5C,
    0xC2,
    0xD3,
    0xAC,
    0x62,
    0x91,
    0x95,
    0xE4,
    0x79,
    0xE7,
    0xC8,
    0x37,
    0x6D,
    0x8D,
    0xD5,
    0x4E,
    0xA9,
    0x6C,
    0x56,
    0xF4,
    0xEA,
    0x65,
    0x7A,
    0xAE,
    0x08,
    0xBA,
    0x78,
    0x25,
    0x2E,
    0x1C,
    0xA6,
    0xB4,
    0xC6,
    0xE8,
    0xDD,
    0x74,
    0x1F,
    0x4B,
    0xBD,
    0x8B,
    0x8A,
    0x70,
    0x3E,
    0xB5,
    0x66,
    0x48,
    0x03,
    0xF6,
    0x0E,
    0x61,
    0x35,
    0x57,
    0xB9,
    0x86,
    0xC1,
    0x1D,
    0x9E,
    0xE1,
    0xF8,
    0x98,
    0x11,
    0x69,
    0xD9,
    0x8E,
    0x94,
    0x9B,
    0x1E,
    0x87,
    0xE9,
    0xCE,
    0x55,
    0x28,
    0xDF,
    0x8C,
    0xA1,
    0x89,
    0x0D,
    0xBF,
    0xE6,
    0x42,
    0x68,
    0x41,
    0x99,
    0x2D,
    0x0F,
    0xB0,
    0x54,
    0xBB,
    0x16,
]

AES_SBOX_INV = [
    0x52,
    0x09,
    0x6A,
    0xD5,
    0x30,
    0x36,
    0xA5,
    0x38,
    0xBF,
    0x40,
    0xA3,
    0x9E,
    0x81,
    0xF3,
    0xD7,
    0xFB,
    0x7C,
    0xE3,
    0x39,
    0x82,
    0x9B,
    0x2F,
    0xFF,
    0x87,
    0x34,
    0x8E,
    0x43,
    0x44,
    0xC4,
    0xDE,
    0xE9,
    0xCB,
    0x54,
    0x7B,
    0x94,
    0x32,
    0xA6,
    0xC2,
    0x23,
    0x3D,
    0xEE,
    0x4C,
    0x95,
    0x0B,
    0x42,
    0xFA,
    0xC3,
    0x4E,
    0x08,
    0x2E,
    0xA1,
    0x66,
    0x28,
    0xD9,
    0x24,
    0xB2,
    0x76,
    0x5B,
    0xA2,
    0x49,
    0x6D,
    0x8B,
    0xD1,
    0x25,
    0x72,
    0xF8,
    0xF6,
    0x64,
    0x86,
    0x68,
    0x98,
    0x16,
    0xD4,
    0xA4,
    0x5C,
    0xCC,
    0x5D,
    0x65,
    0xB6,
    0x92,
    0x6C,
    0x70,
    0x48,
    0x50,
    0xFD,
    0xED,
    0xB9,
    0xDA,
    0x5E,
    0x15,
    0x46,
    0x57,
    0xA7,
    0x8D,
    0x9D,
    0x84,
    0x90,
    0xD8,
    0xAB,
    0x00,
    0x8C,
    0xBC,
    0xD3,
    0x0A,
    0xF7,
    0xE4,
    0x58,
    0x05,
    0xB8,
    0xB3,
    0x45,
    0x06,
    0xD0,
    0x2C,
    0x1E,
    0x8F,
    0xCA,
    0x3F,
    0x0F,
    0x02,
    0xC1,
    0xAF,
    0xBD,
    0x03,
    0x01,
    0x13,
    0x8A,
    0x6B,
    0x3A,
    0x91,
    0x11,
    0x41,
    0x4F,
    0x67,
    0xDC,
    0xEA,
    0x97,
    0xF2,
    0xCF,
    0xCE,
    0xF0,
    0xB4,
    0xE6,
    0x73,
    0x96,
    0xAC,
    0x74,
    0x22,
    0xE7,
    0xAD,
    0x35,
    0x85,
    0xE2,
    0xF9,
    0x37,
    0xE8,
    0x1C,
    0x75,
    0xDF,
    0x6E,
    0x47,
    0xF1,
    0x1A,
    0x71,
    0x1D,
    0x29,
    0xC5,
    0x89,
    0x6F,
    0xB7,
    0x62,
    0x0E,
    0xAA,
    0x18,
    0xBE,
    0x1B,
    0xFC,
    0x56,
    0x3E,
    0x4B,
    0xC6,
    0xD2,
    0x79,
    0x20,
    0x9A,
    0xDB,
    0xC0,
    0xFE,
    0x78,
    0xCD,
    0x5A,
    0xF4,
    0x1F,
    0xDD,
    0xA8,
    0x33,
    0x88,
    0x07,
    0xC7,
    0x31,
    0xB1,
    0x12,
    0x10,
    0x59,
    0x27,
    0x80,
    0xEC,
    0x5F,
    0x60,
    0x51,
    0x7F,
    0xA9,
    0x19,
    0xB5,
    0x4A,
    0x0D,
    0x2D,
    0xE5,
    0x7A,
    0x9F,
    0x93,
    0xC9,
    0x9C,
    0xEF,
    0xA0,
    0xE0,
    0x3B,
    0x4D,
    0xAE,
    0x2A,
    0xF5,
    0xB0,
    0xC8,
    0xEB,
    0xBB,
    0x3C,
    0x83,
    0x53,
    0x99,
    0x61,
    0x17,
    0x2B,
    0x04,
    0x7E,
    0xBA,
    0x77,
    0xD6,
    0x26,
    0xE1,
    0x69,
    0x14,
    0x63,
    0x55,
    0x21,
    0x0C,
    0x7D,
]

AES_RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]


def _aes_xtime(a):
    return ((a << 1) ^ 0x1B) & 0xFF if a & 0x80 else (a << 1) & 0xFF


def _aes_mix_col(r):
    a = [0] * 4
    b = [0] * 4
    for c in range(4):
        a[c] = r[c]
        b[c] = _aes_xtime(r[c])
    r[0] = b[0] ^ a[3] ^ a[2] ^ b[1] ^ a[1]
    r[1] = b[1] ^ a[0] ^ a[3] ^ b[2] ^ a[2]
    r[2] = b[2] ^ a[1] ^ a[0] ^ b[3] ^ a[3]
    r[3] = b[3] ^ a[2] ^ a[1] ^ b[0] ^ a[0]


def aes128_encrypt(plaintext, key):
    """
    AES-128 encrypt a 16-byte block.

    Args:
        plaintext: list of 16 bytes
        key: list of 16 bytes

    Returns:
        list of 16 encrypted bytes
    """
    # Key expansion
    rk = list(key) + [0] * 160
    for i in range(4, 44):
        t = rk[(i - 1) * 4 : i * 4]
        if i % 4 == 0:
            t = [
                AES_SBOX[t[1]] ^ AES_RCON[i // 4 - 1],
                AES_SBOX[t[2]],
                AES_SBOX[t[3]],
                AES_SBOX[t[0]],
            ]
        for j in range(4):
            rk[i * 4 + j] = rk[(i - 4) * 4 + j] ^ t[j]

    state = list(plaintext)

    # AddRoundKey
    for i in range(16):
        state[i] ^= rk[i]

    for rnd in range(1, 11):
        # SubBytes
        state = [AES_SBOX[b] for b in state]
        # ShiftRows
        state[1], state[5], state[9], state[13] = (
            state[5],
            state[9],
            state[13],
            state[1],
        )
        state[2], state[6], state[10], state[14] = (
            state[10],
            state[14],
            state[2],
            state[6],
        )
        state[3], state[7], state[11], state[15] = (
            state[15],
            state[3],
            state[7],
            state[11],
        )
        # MixColumns (not in last round)
        if rnd < 10:
            for c in range(4):
                col = state[c * 4 : c * 4 + 4]
                _aes_mix_col(col)
                state[c * 4 : c * 4 + 4] = col
        # AddRoundKey
        off = rnd * 16
        for i in range(16):
            state[i] ^= rk[off + i]

    return state


def aes128_decrypt(ciphertext, key):
    """
    AES-128 decrypt a 16-byte block.

    Args:
        ciphertext: list of 16 bytes
        key: list of 16 bytes

    Returns:
        list of 16 decrypted bytes
    """
    # Key expansion (same as encrypt)
    rk = list(key) + [0] * 160
    for i in range(4, 44):
        t = rk[(i - 1) * 4 : i * 4]
        if i % 4 == 0:
            t = [
                AES_SBOX[t[1]] ^ AES_RCON[i // 4 - 1],
                AES_SBOX[t[2]],
                AES_SBOX[t[3]],
                AES_SBOX[t[0]],
            ]
        for j in range(4):
            rk[i * 4 + j] = rk[(i - 4) * 4 + j] ^ t[j]

    state = list(ciphertext)

    # AddRoundKey (last round key)
    for i in range(16):
        state[i] ^= rk[160 + i]

    for rnd in range(9, -1, -1):
        # InvShiftRows
        state[1], state[5], state[9], state[13] = (
            state[13],
            state[1],
            state[5],
            state[9],
        )
        state[2], state[6], state[10], state[14] = (
            state[10],
            state[14],
            state[2],
            state[6],
        )
        state[3], state[7], state[11], state[15] = (
            state[7],
            state[11],
            state[15],
            state[3],
        )
        # InvSubBytes
        state = [AES_SBOX_INV[b] for b in state]
        # AddRoundKey
        off = rnd * 16
        for i in range(16):
            state[i] ^= rk[off + i]
        # InvMixColumns (not in first round)
        if rnd > 0:
            for c in range(4):
                col = state[c * 4 : c * 4 + 4]
                # Inverse mix using repeated xtime
                u = _aes_xtime(_aes_xtime(col[0] ^ col[2]))
                v = _aes_xtime(_aes_xtime(col[1] ^ col[3]))
                col[0] ^= u
                col[1] ^= v
                col[2] ^= u
                col[3] ^= v
                _aes_mix_col(col)
                state[c * 4 : c * 4 + 4] = col

    return state


# ═══════════════════════════════════════════════════════════
# AUT64 Block Cipher
# Used by: VAG VW/Audi (older models)
# Key: 64 bits, Block: 64 bits, Rounds: 12
# ═══════════════════════════════════════════════════════════

AUT64_ROUNDS = 12

# Round permutation tables
_AUT64_TABLE_LN = [4, 5, 2, 3, 7, 0, 6, 1, 3, 6, 1, 5]
_AUT64_TABLE_UN = [2, 1, 6, 0, 5, 7, 3, 4, 0, 4, 7, 2]

# Offset table (16x16)
_AUT64_TABLE_OFFSET = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    1,
    0,
    3,
    2,
    5,
    4,
    7,
    6,
    9,
    8,
    11,
    10,
    13,
    12,
    15,
    14,
    2,
    3,
    0,
    1,
    6,
    7,
    4,
    5,
    10,
    11,
    8,
    9,
    14,
    15,
    12,
    13,
    3,
    2,
    1,
    0,
    7,
    6,
    5,
    4,
    11,
    10,
    9,
    8,
    15,
    14,
    13,
    12,
    4,
    5,
    6,
    7,
    0,
    1,
    2,
    3,
    12,
    13,
    14,
    15,
    8,
    9,
    10,
    11,
    5,
    4,
    7,
    6,
    1,
    0,
    3,
    2,
    13,
    12,
    15,
    14,
    9,
    8,
    11,
    10,
    6,
    7,
    4,
    5,
    2,
    3,
    0,
    1,
    14,
    15,
    12,
    13,
    10,
    11,
    8,
    9,
    7,
    6,
    5,
    4,
    3,
    2,
    1,
    0,
    15,
    14,
    13,
    12,
    11,
    10,
    9,
    8,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    9,
    8,
    11,
    10,
    13,
    12,
    15,
    14,
    1,
    0,
    3,
    2,
    5,
    4,
    7,
    6,
    10,
    11,
    8,
    9,
    14,
    15,
    12,
    13,
    2,
    3,
    0,
    1,
    6,
    7,
    4,
    5,
    11,
    10,
    9,
    8,
    15,
    14,
    13,
    12,
    3,
    2,
    1,
    0,
    7,
    6,
    5,
    4,
    12,
    13,
    14,
    15,
    8,
    9,
    10,
    11,
    4,
    5,
    6,
    7,
    0,
    1,
    2,
    3,
    13,
    12,
    15,
    14,
    9,
    8,
    11,
    10,
    5,
    4,
    7,
    6,
    1,
    0,
    3,
    2,
    14,
    15,
    12,
    13,
    10,
    11,
    8,
    9,
    6,
    7,
    4,
    5,
    2,
    3,
    0,
    1,
    15,
    14,
    13,
    12,
    11,
    10,
    9,
    8,
    7,
    6,
    5,
    4,
    3,
    2,
    1,
    0,
]


def aut64_encrypt(data_bytes, key_bytes, sbox, pbox):
    """
    AUT64 encrypt.

    Args:
        data_bytes: list of 8 bytes (64-bit block)
        key_bytes: list of 8 bytes (64-bit key, nibble-indexed)
        sbox: list of 16 substitution values
        pbox: list of 8 permutation indices

    Returns:
        list of 8 encrypted bytes
    """
    state = list(data_bytes)
    for rnd in range(AUT64_ROUNDS):
        ln = _AUT64_TABLE_LN[rnd]
        un = _AUT64_TABLE_UN[rnd]
        # Get nibbles
        lower = state[ln] & 0x0F
        upper = (state[un] >> 4) & 0x0F
        # Offset lookup
        offset = _AUT64_TABLE_OFFSET[upper * 16 + lower]
        # Key nibble
        key_nib = key_bytes[pbox[rnd % 8]] & 0x0F
        # Substitute
        val = sbox[(offset + key_nib) & 0x0F]
        # XOR into state
        state[ln] = (state[ln] & 0xF0) | (val & 0x0F)
    return state


def aut64_decrypt(data_bytes, key_bytes, sbox, pbox):
    """
    AUT64 decrypt (reverse rounds).

    Args:
        Same as aut64_encrypt.

    Returns:
        list of 8 decrypted bytes
    """
    # Build inverse sbox
    inv_sbox = [0] * 16
    for i in range(16):
        inv_sbox[sbox[i]] = i

    state = list(data_bytes)
    for rnd in range(AUT64_ROUNDS - 1, -1, -1):
        ln = _AUT64_TABLE_LN[rnd]
        un = _AUT64_TABLE_UN[rnd]
        lower = state[ln] & 0x0F
        upper = (state[un] >> 4) & 0x0F
        key_nib = key_bytes[pbox[rnd % 8]] & 0x0F
        # Reverse substitute
        orig_offset = (inv_sbox[lower] - key_nib) & 0x0F
        # Reverse offset lookup
        for i in range(16):
            if _AUT64_TABLE_OFFSET[upper * 16 + i] == orig_offset:
                state[ln] = (state[ln] & 0xF0) | i
                break
    return state


# ═══════════════════════════════════════════════════════════
# KIA V5 Mixer Cipher
# Used by: KIA V5
# Encrypted: 32 bits -> Counter: 16 bits
# Key: 64 bits (8 bytes), Rounds: 18 x 8
# ═══════════════════════════════════════════════════════════


def kia_v5_mixer_decrypt(encrypted, key_bytes):
    """
    KIA V5 mixer cipher decrypt.

    Args:
        encrypted: 32-bit encrypted value
        key_bytes: list of 8 key bytes

    Returns:
        16-bit decrypted counter value
    """
    s = [
        (encrypted >> 24) & 0xFF,
        (encrypted >> 16) & 0xFF,
        (encrypted >> 8) & 0xFF,
        encrypted & 0xFF,
    ]

    for rnd in range(17, -1, -1):
        kb = key_bytes[rnd % 8]
        for step in range(7, -1, -1):
            # Select base from state bit
            bit_idx = step % 4
            if (s[bit_idx] >> (step % 8)) & 1:
                base = s[(step + 1) % 4]
            else:
                base = s[(step + 2) % 4]
            # XOR with key and shift
            val = (base ^ kb) & 0xFF
            s[step % 4] = (s[step % 4] ^ (val >> (step % 4))) & 0xFF

    return (s[0] << 8) | s[1]


# ═══════════════════════════════════════════════════════════
# Mitsubishi V0 XOR Scrambling
# Used by: Mitsubishi V0
# Input: byte array + 16-bit counter
# ═══════════════════════════════════════════════════════════


def mitsubishi_v0_scramble(payload, counter):
    """
    Mitsubishi V0 XOR scramble.

    Args:
        payload: list of bytes (at least 8)
        counter: 16-bit counter

    Returns:
        list of scrambled bytes
    """
    result = list(payload)
    hi = (counter >> 8) & 0xFF
    lo = counter & 0xFF

    mask1 = (hi & 0xAA) | (lo & 0x55)
    mask2 = (lo & 0xAA) | (hi & 0x55)
    mask3 = mask1 ^ mask2

    # XOR first 5 bytes with mask3
    for i in range(min(5, len(result))):
        result[i] ^= mask3

    # Invert first 8 bytes
    for i in range(min(8, len(result))):
        result[i] = (~result[i]) & 0xFF

    return result


def mitsubishi_v0_descramble(payload, counter):
    """
    Mitsubishi V0 XOR descramble (reverse of scramble).
    Since invert is its own inverse and XOR is its own inverse,
    just apply the same operations in reverse order.
    """
    result = list(payload)

    # Un-invert first 8 bytes
    for i in range(min(8, len(result))):
        result[i] = (~result[i]) & 0xFF

    # Un-XOR first 5 bytes
    hi = (counter >> 8) & 0xFF
    lo = counter & 0xFF
    mask1 = (hi & 0xAA) | (lo & 0x55)
    mask2 = (lo & 0xAA) | (hi & 0x55)
    mask3 = mask1 ^ mask2
    for i in range(min(5, len(result))):
        result[i] ^= mask3

    return result


# ═══════════════════════════════════════════════════════════
# Ford V0 GF(2) Matrix CRC
# Used by: Ford V0 car keys
# Matrix: 8x8 bytes, Output: 8-bit CRC
# ═══════════════════════════════════════════════════════════

FORD_V0_CRC_MATRIX = [
    0xDA,
    0xB5,
    0x55,
    0x6A,
    0xAA,
    0xAA,
    0xAA,
    0xD5,
    0xB6,
    0x6C,
    0xCC,
    0xD9,
    0x99,
    0x99,
    0x99,
    0xB3,
    0x71,
    0xE3,
    0xC3,
    0xC7,
    0x87,
    0x87,
    0x87,
    0x8F,
    0x0F,
    0xE0,
    0x3F,
    0xC0,
    0x7F,
    0x80,
    0x7F,
    0x80,
    0x00,
    0x1F,
    0xFF,
    0xC0,
    0x00,
    0x7F,
    0xFF,
    0x80,
    0x00,
    0x00,
    0x00,
    0x3F,
    0xFF,
    0xFF,
    0xFF,
    0x80,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x7F,
    0x23,
    0x12,
    0x94,
    0x84,
    0x35,
    0xF4,
    0x55,
    0x84,
]


def _popcount8(x):
    count = 0
    while x:
        count += x & 1
        x >>= 1
    return count


def ford_v0_calculate_crc(buf):
    """
    Ford V0 GF(2) matrix CRC.

    Args:
        buf: list of at least 9 bytes (bytes 1-8 used)

    Returns:
        8-bit CRC value
    """
    crc = 0
    for row in range(8):
        xor_sum = 0
        for col in range(8):
            xor_sum ^= FORD_V0_CRC_MATRIX[row * 8 + col] & buf[col + 1]
        if _popcount8(xor_sum) & 1:
            crc |= 1 << row
    return crc


def ford_v0_calculate_bs(counter, button, bs_magic=0x6F):
    """
    Ford V0 BS (checksum byte) calculation.

    Args:
        counter: counter value (low byte used)
        button: 4-bit button code
        bs_magic: magic constant (default 0x6F)

    Returns:
        8-bit BS value
    """
    return ((counter & 0xFF) + bs_magic + (button << 4)) & 0xFF


# ═══════════════════════════════════════════════════════════
# PSA Second-Stage XOR Permutation
# Used by: PSA Peugeot/Citroen
# Input: 6-byte buffer
# ═══════════════════════════════════════════════════════════


def psa_xor_encrypt(buf):
    """
    PSA second-stage XOR permutation encrypt.

    Args:
        buf: list of at least 7 bytes (indices 0-6)

    Returns:
        list of encrypted bytes
    """
    result = list(buf)
    e = list(buf)
    e[6] = result[5] ^ e[6] ^ e[5]  # placeholder
    e[0] = result[2] ^ e[5]
    e[2] = result[4] ^ e[0]
    e[4] = result[3] ^ e[2]
    e[3] = result[0] ^ e[5]
    e[1] = result[1] ^ e[3]
    return e


def psa_xor_decrypt(buf):
    """
    PSA second-stage XOR permutation decrypt.

    Args:
        buf: list of at least 7 encrypted bytes

    Returns:
        list of decrypted bytes
    """
    e = list(buf)
    result = [0] * len(buf)
    result[1] = e[1] ^ e[3]
    result[0] = e[3] ^ e[5]
    result[3] = e[4] ^ e[2]
    result[4] = e[2] ^ e[0]
    result[2] = e[0] ^ e[5]
    result[5] = e[6] ^ e[5] ^ e[6]
    for i in range(7, len(buf)):
        result[i] = buf[i]
    return result


# ═══════════════════════════════════════════════════════════
# CRC utilities
# ═══════════════════════════════════════════════════════════


def crc8(data, poly=0x07, init=0x00):
    """
    Generic CRC-8.

    Args:
        data: list of bytes
        poly: polynomial (default 0x07)
        init: initial value

    Returns:
        8-bit CRC
    """
    crc = init
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ poly) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc


def crc16_ccitt(data, poly=0x8005, init=0x0000):
    """
    CRC-16 CCITT.

    Args:
        data: list of bytes
        poly: polynomial (default 0x8005)
        init: initial value

    Returns:
        16-bit CRC
    """
    crc = init
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ poly) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


# ═══════════════════════════════════════════════════════════
# Available ciphers registry
# ═══════════════════════════════════════════════════════════

CIPHER_INFO = {
    "TEA": {
        "name": "TEA (Tiny Encryption Algorithm)",
        "key_bits": 128,
        "block_bits": 64,
        "used_by": "PSA Peugeot/Citroen, VAG VW/Audi",
    },
    "AES-128": {
        "name": "AES-128",
        "key_bits": 128,
        "block_bits": 128,
        "used_by": "KIA V6, Hyundai",
    },
    "AUT64": {
        "name": "AUT64",
        "key_bits": 64,
        "block_bits": 64,
        "used_by": "VAG VW/Audi (older)",
    },
    "KIA-V5-Mixer": {
        "name": "KIA V5 Mixer Cipher",
        "key_bits": 64,
        "block_bits": 32,
        "used_by": "KIA V5",
    },
    "Mitsubishi-XOR": {
        "name": "Mitsubishi V0 XOR Scrambling",
        "key_bits": 16,
        "block_bits": 64,
        "used_by": "Mitsubishi V0",
    },
    "Ford-GF2-CRC": {
        "name": "Ford V0 GF(2) Matrix CRC",
        "key_bits": 0,
        "block_bits": 8,
        "used_by": "Ford V0",
    },
    "KeeLoq": {
        "name": "KeeLoq",
        "key_bits": 64,
        "block_bits": 32,
        "used_by": "HCS200/300, FAAC, NICE, StarLine, many gates",
    },
}
