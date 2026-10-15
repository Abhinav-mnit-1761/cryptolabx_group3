# ==============================================================================
# CRYPTOGRAPHIC PRIME GENERATION USING MILLER-RABIN PRIMALITY TEST
# ==============================================================================
# Module: miller_rabin.py
# Description: Implementation of 512-bit probable prime generation using the
#              Miller-Rabin probabilistic primality test, small prime pre-filtering,
#              and independent mathematical verification (Fermat test, trial
#              division, and Strong Lucas test).
# ==============================================================================

import math
import secrets
import time


def sieve_small_primes(limit=1000):
    """Generate a list of small prime numbers up to `limit` using Sieve of Eratosthenes."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(math.isqrt(limit)) + 1):
        if is_prime[p]:
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False
    return [p for p, prime in enumerate(is_prime) if prime]


# Precomputed list of primes up to 1000 (168 primes)
SMALL_PRIMES = sieve_small_primes(1000)


def generate_candidate(bit_length=512):
    """
    Generate a random odd candidate integer of exactly `bit_length` bits.
    
    1. Generates `bit_length` cryptographically secure random bits.
    2. Sets the Most Significant Bit (MSB, bit bit_length - 1) to 1 to guarantee
       the exact bit length.
    3. Sets the Least Significant Bit (LSB, bit 0) to 1 to ensure the candidate is odd.
    """
    candidate = secrets.randbits(bit_length)
    candidate |= (1 << (bit_length - 1))  # Ensure exact bit length
    candidate |= 1                        # Ensure number is odd
    return candidate


def is_small_prime_divisible(n, small_primes=None):
    """
    Quick pre-filter: test divisibility against small primes.
    Eliminates ~90% of composite numbers instantly before costly exponentiations.
    """
    if small_primes is None:
        small_primes = SMALL_PRIMES
    for p in small_primes:
        if n == p:
            return False
        if n % p == 0:
            return True
    return False


def decompose(n):
    """
    Decompose n - 1 into 2^s * d, where d is an odd positive integer.
    """
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    return s, d


def miller_rabin_round(n, a, s=None, d=None):
    """
    Perform a single Miller-Rabin primality test round on odd candidate `n` with base `a`.
    
    Returns:
        (passed: bool, message: str)
    """
    if s is None or d is None:
        s, d = decompose(n)

    # Check for non-trivial GCD factor
    g = math.gcd(a, n)
    if 1 < g < n:
        return False, f"Base {a}: Failed (gcd({a}, n) = {g} > 1, factor found)"

    # Compute x_0 = a^d mod n
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True, f"Base {a}: Passed at initial test (a^d mod n == {x})"

    # Square x repeatedly up to s - 1 times
    for r in range(1, s):
        x = pow(x, 2, n)
        if x == n - 1:
            return True, f"Base {a}: Passed at square step {r} (a^(d*2^{r}) mod n == n - 1)"
        if x == 1:
            return False, f"Base {a}: Failed (non-trivial square root of 1 modulo n)"

    return False, f"Base {a}: Failed (a^(n-1) != 1 mod n)"


def miller_rabin_test(n, rounds=40, custom_bases=None):
    """
    Test primality of n using the Miller-Rabin test with multiple bases.
    
    For a candidate composite number, each independent round with a random base
    has a failure probability <= 1/4. With 40 rounds, the probability that a
    composite number passes all rounds is <= (1/4)^40 = 2^(-80) < 10^(-24).
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    s, d = decompose(n)

    if custom_bases is not None:
        bases = [b for b in custom_bases if 2 <= b <= n - 2]
    else:
        max_possible_bases = n - 3
        target_rounds = min(rounds, max_possible_bases)

        # Standard small prime bases followed by random bases
        standard_bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
        bases = [b for b in standard_bases if 2 <= b <= n - 2]
        used = set(bases)

        while len(bases) < target_rounds and len(used) < max_possible_bases:
            a = secrets.randbelow(n - 3) + 2
            if a not in used:
                used.add(a)
                bases.append(a)

    if not bases:
        # For n = 3, bases is empty and handled by edge case above
        return True

    for a in bases:
        passed, _ = miller_rabin_round(n, a, s, d)
        if not passed:
            return False

    return True


def generate_prime(bit_length=512, rounds=40, use_prefilter=True):
    """
    Generate a probable prime integer of exactly `bit_length` bits using Miller-Rabin.
    
    Returns:
        (prime: int, stats: dict)
    """
    start_time = time.perf_counter()
    candidates_tested = 0
    prefilter_rejected = 0
    mr_tested = 0

    while True:
        candidate = generate_candidate(bit_length)
        candidates_tested += 1

        # Step 1: Pre-filter with small primes trial division
        if use_prefilter and is_small_prime_divisible(candidate):
            prefilter_rejected += 1
            continue

        # Step 2: Miller-Rabin primality test
        mr_tested += 1
        if miller_rabin_test(candidate, rounds=rounds):
            total_time = time.perf_counter() - start_time
            stats = {
                'assigned_bit_length': bit_length,
                'actual_bit_length': candidate.bit_length(),
                'candidates_tested': candidates_tested,
                'prefilter_rejected': prefilter_rejected,
                'mr_candidates_tested': mr_tested,
                'mr_rounds': rounds,
                'execution_time': total_time,
                'candidate': candidate,
                'hex': hex(candidate),
            }
            return candidate, stats


# ==============================================================================
# INDEPENDENT VERIFICATION METHODS
# ==============================================================================

def fermat_primality_test(n, bases=None):
    """
    Independent Check: Fermat's Little Theorem Test.
    For prime n and any base a coprime to n: a^(n - 1) = 1 (mod n).
    """
    if n < 2:
        return False, []
    if bases is None:
        # Independent set of prime bases distinct from initial MR bases
        bases = [41, 43, 47, 53, 59, 61, 67, 71, 73, 79]

    results = []
    for a in bases:
        if a >= n:
            continue
        if math.gcd(a, n) != 1:
            return False, [(a, False, 'Not coprime')]
        res = pow(a, n - 1, n)
        is_valid = (res == 1)
        results.append((a, is_valid, res))
        if not is_valid:
            return False, results
    return True, results


def trial_division_check(n, limit=2000):
    """
    Independent Check: Trial division against all primes up to `limit`.
    Ensures candidate has no small prime factors.
    """
    primes = sieve_small_primes(limit)
    for p in primes:
        if n == p:
            return True, None
        if n % p == 0:
            return False, p
    return True, None


def jacobi_symbol(a, n):
    """Compute the Jacobi symbol (a / n) for odd n > 0."""
    a = a % n
    t = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                t = -t
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            t = -t
        a = a % n
    return t if n == 1 else 0


def strong_lucas_test(n):
    """
    Independent Check: Strong Lucas Probable Prime Test (Selfridge Parameter Method A).
    When combined with Miller-Rabin base 2, forms the Baillie-PSW primality test.
    There are NO known composite numbers that pass Baillie-PSW!
    """
    if n <= 1:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Check perfect square
    s = math.isqrt(n)
    if s * s == n:
        return False

    # Find D in 5, -7, 9, -11, 13, ... with Jacobi(D, n) == -1
    D = 5
    while True:
        j = jacobi_symbol(D, n)
        if j == -1:
            break
        if j == 0:
            g = math.gcd(abs(D), n)
            if 1 < g < n:
                return False
        D = -(D + 2) if D > 0 else -(D - 2)
        if abs(D) > 2000:
            return False

    P = 1
    Q = (1 - D) // 4

    # Decompose n + 1 = 2^s * d, with d odd
    d = n + 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    inv2 = (n + 1) // 2

    # Binary chain for Lucas sequence values U_d, V_d, Q^d mod n
    u = 1
    v = P
    q = Q
    bits = bin(d)[3:]  # Skip '0b1'

    for bit in bits:
        # Double: k -> 2k
        u_new = (u * v) % n
        v_new = (v * v - 2 * q) % n
        q_new = (q * q) % n
        u, v, q = u_new, v_new, q_new

        if bit == '1':
            # Add 1: 2k -> 2k + 1
            u_new = ((u + v) * inv2) % n
            v_new = ((D * u + v) * inv2) % n
            q_new = (q * Q) % n
            u, v, q = u_new, v_new, q_new

    if u == 0 or v == 0:
        return True

    for _ in range(1, s):
        v = (v * v - 2 * q) % n
        q = (q * q) % n
        if v == 0:
            return True

    return False


def verify_prime(n, assigned_bit_length=512, specified_bases=None):
    """
    Perform comprehensive multi-layer verification:
    1. Bit length check (exact match to assigned bit length)
    2. Miller-Rabin test on specified deterministic bases
    3. Trial division against small primes up to 2000
    4. Independent Fermat's Little Theorem test on separate bases
    5. Independent Strong Lucas primality test (Baillie-PSW)
    """
    if specified_bases is None:
        specified_bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

    actual_bit_length = n.bit_length()
    bit_length_valid = (actual_bit_length == assigned_bit_length)

    s, d = decompose(n)
    mr_base_results = []
    all_mr_passed = True
    for a in specified_bases:
        if a >= n - 1:
            continue
        passed, msg = miller_rabin_round(n, a, s, d)
        mr_base_results.append({'base': a, 'passed': passed, 'message': msg})
        if not passed:
            all_mr_passed = False

    trial_passed, factor = trial_division_check(n, limit=2000)
    fermat_passed, fermat_details = fermat_primality_test(n)
    lucas_passed = strong_lucas_test(n)

    overall_valid = (bit_length_valid and all_mr_passed and trial_passed and
                     fermat_passed and lucas_passed)

    return {
        'candidate': n,
        'assigned_bit_length': assigned_bit_length,
        'actual_bit_length': actual_bit_length,
        'bit_length_valid': bit_length_valid,
        's_exponent': s,
        'd_odd_component': d,
        'mr_specified_bases': mr_base_results,
        'all_mr_passed': all_mr_passed,
        'trial_division_passed': trial_passed,
        'trial_division_factor': factor,
        'fermat_test_passed': fermat_passed,
        'fermat_details': fermat_details,
        'strong_lucas_passed': lucas_passed,
        'overall_verified': overall_valid
    }
