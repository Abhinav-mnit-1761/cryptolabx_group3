"""
Unit and Integration Tests for Padding Oracle Attack
====================================================
Tests PKCS#7 padding validation, oracle behavior, edge cases,
and full multi-block plaintext recovery.
"""

import sys
import os
import unittest

# Ensure local imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "..", "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from aes_cipher import (
    pkcs7_pad,
    pkcs7_unpad,
    is_pkcs7_valid,
    PaddingOracle
)
from padding_oracle_attack import recover_block, padding_oracle_attack


class TestPKCS7(unittest.TestCase):
    def test_pad_basic(self):
        data = b"YELLOW SUBMARINE"  # Exactly 16 bytes
        padded = pkcs7_pad(data, 16)
        self.assertEqual(len(padded), 32)
        self.assertEqual(padded[-16:], bytes([16] * 16))
        self.assertEqual(pkcs7_unpad(padded, 16), data)

    def test_pad_partial(self):
        data = b"HELLO"  # 5 bytes
        padded = pkcs7_pad(data, 16)
        self.assertEqual(len(padded), 16)
        self.assertEqual(padded[-11:], bytes([11] * 11))
        self.assertEqual(pkcs7_unpad(padded, 16), data)

    def test_invalid_padding(self):
        bad1 = b"123456789012345\x00"  # pad len 0 invalid
        bad2 = b"12345678901234\x02\x03"  # mismatched bytes
        bad3 = b"123456789012345\x11"  # pad len 17 > 16
        self.assertFalse(is_pkcs7_valid(bad1, 16))
        self.assertFalse(is_pkcs7_valid(bad2, 16))
        self.assertFalse(is_pkcs7_valid(bad3, 16))


class TestPaddingOracleAttack(unittest.TestCase):
    def setUp(self):
        self.oracle = PaddingOracle()

    def test_oracle_feedback(self):
        msg = b"Top secret clearance level 5"
        iv, ct = self.oracle.encrypt_message(msg)
        self.assertTrue(self.oracle.is_padding_valid(iv, ct))

        # Corrupt the last byte of ciphertext
        corrupted = bytearray(ct)
        corrupted[-1] ^= 0x33
        self.assertFalse(self.oracle.is_padding_valid(iv, bytes(corrupted)))

    def test_single_byte_message(self):
        msg = b"A"
        iv, ct = self.oracle.encrypt_message(msg)
        res = padding_oracle_attack(self.oracle, iv, ct, block_size=16, verbose=False)
        self.assertEqual(res["plaintext"], msg)

    def test_exact_block_boundary(self):
        msg = b"0123456789ABCDEF"  # 16 bytes
        iv, ct = self.oracle.encrypt_message(msg)
        res = padding_oracle_attack(self.oracle, iv, ct, block_size=16, verbose=False)
        self.assertEqual(res["plaintext"], msg)

    def test_multi_block_recovery(self):
        msg = b"Cryptographic security relies on authenticated encryption!"
        iv, ct = self.oracle.encrypt_message(msg)
        res = padding_oracle_attack(self.oracle, iv, ct, block_size=16, verbose=False)
        self.assertEqual(res["plaintext"], msg)
        self.assertGreater(res["total_queries"], 0)


if __name__ == "__main__":
    unittest.main()
