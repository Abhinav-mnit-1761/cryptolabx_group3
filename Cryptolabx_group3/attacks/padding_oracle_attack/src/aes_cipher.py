"""
AES-CBC Cipher, PKCS#7 Padding, and Padding Oracle Simulation
Supports hardware-accelerated `cryptography` library when available,
with automatic fallback to a pure-Python NIST FIPS-197 AES-128 engine
requiring zero external dependencies.
"""

import os

# Check for cryptography library
try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    _HAS_CRYPTOGRAPHY = True
except ImportError:
    _HAS_CRYPTOGRAPHY = False

# =====================================================================
# Pure Python AES-128 Fallback (NIST FIPS 197 Compliant)
# =====================================================================

_SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

_INV_SBOX = [0] * 256
for _i, _v in enumerate(_SBOX):
    _INV_SBOX[_v] = _i

_RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

def _xtime(a: int) -> int:
    return (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

def _mul(a: int, b: int) -> int:
    res = 0
    while b:
        if b & 1:
            res ^= a
        a = _xtime(a)
        b >>= 1
    return res

def _aes128_key_expansion(key: bytes) -> list[list[int]]:
    w = list(key)
    for i in range(4, 44):
        temp = w[(i - 1) * 4 : i * 4]
        if i % 4 == 0:
            temp = [_SBOX[temp[1]], _SBOX[temp[2]], _SBOX[temp[3]], _SBOX[temp[0]]]
            temp[0] ^= _RCON[i // 4]
        for j in range(4):
            w.append(w[(i - 4) * 4 + j] ^ temp[j])
    return [w[i * 16 : (i + 1) * 16] for i in range(11)]

def _aes128_encrypt_block(pt: bytes, round_keys: list[list[int]]) -> bytes:
    state = [s ^ k for s, k in zip(pt, round_keys[0])]
    for r in range(1, 10):
        state = [_SBOX[b] for b in state]
        state = [
            state[0], state[5], state[10], state[15],
            state[4], state[9], state[14], state[3],
            state[8], state[13], state[2], state[7],
            state[12], state[1], state[6], state[11]
        ]
        new_state = [0] * 16
        for c in range(4):
            idx = c * 4
            s0, s1, s2, s3 = state[idx : idx + 4]
            new_state[idx]     = _xtime(s0) ^ (_xtime(s1) ^ s1) ^ s2 ^ s3
            new_state[idx + 1] = s0 ^ _xtime(s1) ^ (_xtime(s2) ^ s2) ^ s3
            new_state[idx + 2] = s0 ^ s1 ^ _xtime(s2) ^ (_xtime(s3) ^ s3)
            new_state[idx + 3] = (_xtime(s0) ^ s0) ^ s1 ^ s2 ^ _xtime(s3)
        state = [s ^ k for s, k in zip(new_state, round_keys[r])]
    state = [_SBOX[b] for b in state]
    state = [
        state[0], state[5], state[10], state[15],
        state[4], state[9], state[14], state[3],
        state[8], state[13], state[2], state[7],
        state[12], state[1], state[6], state[11]
    ]
    state = [s ^ k for s, k in zip(state, round_keys[10])]
    return bytes(state)

def _aes128_decrypt_block(ct: bytes, round_keys: list[list[int]]) -> bytes:
    state = [s ^ k for s, k in zip(ct, round_keys[10])]
    for r in range(9, 0, -1):
        state = [
            state[0], state[13], state[10], state[7],
            state[4], state[1], state[14], state[11],
            state[8], state[5], state[2], state[15],
            state[12], state[9], state[6], state[3]
        ]
        state = [_INV_SBOX[b] for b in state]
        state = [s ^ k for s, k in zip(state, round_keys[r])]
        new_state = [0] * 16
        for c in range(4):
            idx = c * 4
            s0, s1, s2, s3 = state[idx : idx + 4]
            new_state[idx]     = _mul(s0, 0x0e) ^ _mul(s1, 0x0b) ^ _mul(s2, 0x0d) ^ _mul(s3, 0x09)
            new_state[idx + 1] = _mul(s0, 0x09) ^ _mul(s1, 0x0e) ^ _mul(s2, 0x0b) ^ _mul(s3, 0x0d)
            new_state[idx + 2] = _mul(s0, 0x0d) ^ _mul(s1, 0x09) ^ _mul(s2, 0x0e) ^ _mul(s3, 0x0b)
            new_state[idx + 3] = _mul(s0, 0x0b) ^ _mul(s1, 0x0d) ^ _mul(s2, 0x09) ^ _mul(s3, 0x0e)
        state = new_state
    state = [
        state[0], state[13], state[10], state[7],
        state[4], state[1], state[14], state[11],
        state[8], state[5], state[2], state[15],
        state[12], state[9], state[6], state[3]
    ]
    state = [_INV_SBOX[b] for b in state]
    state = [s ^ k for s, k in zip(state, round_keys[0])]
    return bytes(state)

# =====================================================================
# PKCS#7 Padding Utilities
# =====================================================================

def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    """Pads data to a multiple of block_size using PKCS#7 standard."""
    if block_size < 1 or block_size > 255:
        raise ValueError("Block size must be between 1 and 255.")
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)

def is_pkcs7_valid(data: bytes, block_size: int = 16) -> bool:
    """Returns True if the byte sequence has valid PKCS#7 padding, False otherwise."""
    if len(data) == 0 or (len(data) % block_size != 0):
        return False
    pad_len = data[-1]
    if pad_len < 1 or pad_len > block_size:
        return False
    return data[-pad_len:] == bytes([pad_len] * pad_len)

def pkcs7_unpad(data: bytes, block_size: int = 16) -> bytes:
    """Removes PKCS#7 padding from data. Raises ValueError if padding is invalid."""
    if not is_pkcs7_valid(data, block_size):
        raise ValueError("Invalid PKCS#7 padding")
    pad_len = data[-1]
    return data[:-pad_len]

# =====================================================================
# AES-CBC Operations
# =====================================================================

def aes_cbc_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    """Encrypts plaintext using AES-128-CBC mode."""
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes for AES-128.")
    if len(iv) != 16:
        raise ValueError("IV must be 16 bytes.")
    if len(plaintext) % 16 != 0:
        raise ValueError("Plaintext length must be a multiple of 16 (pad first).")

    if _HAS_CRYPTOGRAPHY:
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        return encryptor.update(plaintext) + encryptor.finalize()
    else:
        round_keys = _aes128_key_expansion(key)
        blocks = [plaintext[i : i + 16] for i in range(0, len(plaintext), 16)]
        ciphertext = bytearray()
        prev = iv
        for block in blocks:
            xored = bytes(p ^ c for p, c in zip(block, prev))
            encrypted_block = _aes128_encrypt_block(xored, round_keys)
            ciphertext.extend(encrypted_block)
            prev = encrypted_block
        return bytes(ciphertext)

def aes_cbc_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    """Decrypts ciphertext using AES-128-CBC mode."""
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes for AES-128.")
    if len(iv) != 16:
        raise ValueError("IV must be 16 bytes.")
    if len(ciphertext) % 16 != 0:
        raise ValueError("Ciphertext length must be a multiple of 16.")

    if _HAS_CRYPTOGRAPHY:
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()
    else:
        round_keys = _aes128_key_expansion(key)
        blocks = [ciphertext[i : i + 16] for i in range(0, len(ciphertext), 16)]
        plaintext = bytearray()
        prev = iv
        for block in blocks:
            decrypted_block = _aes128_decrypt_block(block, round_keys)
            pt_block = bytes(d ^ p for d, p in zip(decrypted_block, prev))
            plaintext.extend(pt_block)
            prev = block
        return bytes(plaintext)

# =====================================================================
# Padding Oracle Class
# =====================================================================

class PaddingOracle:
    """
    Simulates a secure server holding a secret AES key.
    The key is strictly encapsulated and NEVER revealed to the attacker.
    Provides a padding verification endpoint that returns a 1-bit boolean:
    True (Valid PKCS#7 Padding) or False (Invalid Padding).
    """

    def __init__(self, key: bytes | None = None):
        self._key = key if key is not None else os.urandom(16)
        self.query_count = 0

    def reset_query_count(self) -> None:
        """Resets the oracle query counter to 0."""
        self.query_count = 0

    def get_query_count(self) -> int:
        """Returns the total number of oracle queries made."""
        return self.query_count

    def encrypt_message(self, plaintext: bytes) -> tuple[bytes, bytes]:
        """
        Server helper: pads and encrypts a message under the secret key.
        Returns (iv, ciphertext).
        """
        iv = os.urandom(16)
        padded = pkcs7_pad(plaintext, 16)
        ciphertext = aes_cbc_encrypt(padded, self._key, iv)
        return iv, ciphertext

    def is_padding_valid(self, iv: bytes, ciphertext: bytes) -> bool:
        """
        The Oracle Endpoint:
        Decrypts (iv, ciphertext) using the private key and returns True if
        the decrypted plaintext has valid PKCS#7 padding, or False otherwise.
        Tracks query count.
        """
        self.query_count += 1
        try:
            decrypted = aes_cbc_decrypt(ciphertext, self._key, iv)
            return is_pkcs7_valid(decrypted, block_size=16)
        except Exception:
            return False
