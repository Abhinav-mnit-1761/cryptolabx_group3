# ==============================================================================
# UNIT TESTS FOR MILLER-RABIN PRIME GENERATION AND VERIFICATION
# ==============================================================================

import unittest
import sys
import os

# Add parent directory to path so miller_rabin can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from miller_rabin import (
    generate_candidate,
    decompose,
    miller_rabin_test,
    miller_rabin_round,
    is_small_prime_divisible,
    fermat_primality_test,
    trial_division_check,
    strong_lucas_test,
    verify_prime,
    generate_prime
)


class TestMillerRabin(unittest.TestCase):

    def test_candidate_properties(self):
        """Test candidate generation preserves exact bit length and odd parity."""
        for bit_len in [32, 64, 128, 256, 512]:
            for _ in range(5):
                candidate = generate_candidate(bit_len)
                self.assertEqual(candidate.bit_length(), bit_len, f"Bit length should be {bit_len}")
                self.assertEqual(candidate % 2, 1, "Candidate must be odd")
                self.assertTrue(2**(bit_len - 1) <= candidate < 2**bit_len)

    def test_decompose(self):
        """Test decomposition n - 1 = 2^s * d with odd d."""
        test_cases = [
            (13, 2, 3),    # 13 - 1 = 12 = 4 * 3 = 2^2 * 3
            (17, 4, 1),    # 17 - 1 = 16 = 2^4 * 1
            (25, 3, 3),    # 25 - 1 = 24 = 8 * 3 = 2^3 * 3
            (41, 3, 5),    # 41 - 1 = 40 = 8 * 5 = 2^3 * 5
        ]
        for n, expected_s, expected_d in test_cases:
            s, d = decompose(n)
            self.assertEqual(s, expected_s)
            self.assertEqual(d, expected_d)
            self.assertEqual((2**s) * d, n - 1)
            self.assertEqual(d % 2, 1)

    def test_known_small_primes(self):
        """Verify known primes pass Miller-Rabin test."""
        known_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 97, 1009, 7919]
        for p in known_primes:
            self.assertTrue(miller_rabin_test(p, rounds=20), f"{p} should be prime")

    def test_known_composites(self):
        """Verify known composite numbers fail Miller-Rabin test."""
        known_composites = [4, 6, 8, 9, 10, 12, 14, 15, 21, 25, 27, 33, 35, 100, 1001, 7921]
        for c in known_composites:
            self.assertFalse(miller_rabin_test(c, rounds=20), f"{c} should be composite")

    def test_carmichael_numbers(self):
        """Carmichael numbers pass Fermat test for coprime bases but must FAIL Miller-Rabin."""
        carmichael_numbers = [561, 1105, 1729, 2465, 2821]
        for cn in carmichael_numbers:
            self.assertFalse(miller_rabin_test(cn, rounds=20), f"Carmichael number {cn} must fail Miller-Rabin")

    def test_known_large_primes(self):
        """Verify known large primes (Mersenne primes) pass."""
        mersenne_primes = [
            (2**13) - 1,   # 8191
            (2**17) - 1,   # 131071
            (2**19) - 1,   # 524287
            (2**31) - 1,   # 2147483647
        ]
        for mp in mersenne_primes:
            self.assertTrue(miller_rabin_test(mp, rounds=20), f"Mersenne prime {mp} must pass")

    def test_independent_verification_methods(self):
        """Test Fermat, small prime trial division, and Strong Lucas methods."""
        prime = 65537
        self.assertTrue(trial_division_check(prime)[0])
        self.assertTrue(fermat_primality_test(prime)[0])
        self.assertTrue(strong_lucas_test(prime))

        composite = 561
        # Trial division catches 561 (divisible by 3)
        self.assertFalse(trial_division_check(composite)[0])
        # Strong Lucas test catches 561 as composite
        self.assertFalse(strong_lucas_test(composite))

    def test_prime_generation_and_verification_512(self):
        """Generate a 512-bit prime and run full verification suite."""
        prime, stats = generate_prime(bit_length=512, rounds=40)
        self.assertEqual(prime.bit_length(), 512)
        self.assertEqual(stats['assigned_bit_length'], 512)
        self.assertEqual(stats['actual_bit_length'], 512)
        self.assertGreater(stats['candidates_tested'], 0)

        v_report = verify_prime(prime, assigned_bit_length=512)
        self.assertTrue(v_report['bit_length_valid'])
        self.assertTrue(v_report['all_mr_passed'])
        self.assertTrue(v_report['trial_division_passed'])
        self.assertTrue(v_report['fermat_test_passed'])
        self.assertTrue(v_report['strong_lucas_passed'])
        self.assertTrue(v_report['overall_verified'])


if __name__ == "__main__":
    unittest.main()
