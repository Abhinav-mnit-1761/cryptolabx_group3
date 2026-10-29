Laboratory Notebook — Cryptographic Prime Generation Using Miller–Rabin
Aim
To implement and execute cryptographic prime generation using the Miller–Rabin primality test to generate a 512-bit probable prime, verify that the generated candidate strictly matches the assigned 512-bit length, validate its primality against assigned deterministic bases, and independently verify the prime candidate using small prime trial division, Fermat's Little Theorem test, and the Strong Lucas (Baillie–PSW) test.
Brief Theory
Asymmetric cryptographic schemes such as RSA, Diffie–Hellman, and DSA require large, secret prime numbers to ensure computational security. Deterministic primality tests or trial division for 512-bit integers are computationally infeasible because trial division requires checking prime factors up to sqrt(n) ≈ 2^256 ≈ 1.15 × 10^77 operations. Cryptographic systems instead generate random candidates and verify them using probabilistic polynomial-time algorithms. Fermat's Little Theorem (a^(n-1) ≡ 1 mod n) is insufficient because composite Carmichael numbers (561, 1105, 1729) satisfy Fermat's congruency for all coprime bases. The Miller–Rabin test overcomes this by checking for non-trivial square roots of 1 mod n. For any odd candidate n > 3, n - 1 is decomposed into 2^s · d where d is odd and s >= 1. For any chosen base a in [2, n - 2]:
1. Compute x = a^d mod n. If x ≡ 1 or x ≡ n - 1 mod n, n passes the round.
2. Otherwise, iteratively square x = x^2 mod n up to s - 1 times. If x ≡ n - 1 mod n at any step, n passes the round.
3. If x ≡ 1 mod n is encountered prior to n - 1, or the squarings complete without ever reaching n - 1, then n is composite and a serves as a witness to compositeness.
For every odd composite integer, at least 3/4 of all valid bases act as compositeness witnesses. By executing k = 40 independent rounds, the probability of falsely accepting a composite number is bounded by (1/4)^40 = 2^-80 ≈ 8.27 × 10^-25, satisfying FIPS 186-4 cryptographic criteria.
Algorithm / Flowchart
Algorithm
1. Set the target bit length B = 512 and testing rounds k = 40.
2. Generate a random 512-bit candidate n using a cryptographically secure random number generator.
3. Enforce the Most Significant Bit (MSB, bit 511 = 1) to guarantee exact 512-bit length (2^511 <= n < 2^512) and Least Significant Bit (LSB, bit 0 = 1) to guarantee odd parity.
4. Pre-filter candidate n by trial division against small primes up to 1000 (168 primes); if divisible, discard n and regenerate.
5. Decompose n - 1 into 2^s · d, where d is odd and s >= 1.
6. For each base a in assigned deterministic bases {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37} followed by random bases in [2, n - 2] up to k rounds:
   a. Compute x = a^d mod n.
   b. If x = 1 or x = n - 1, base passes; advance to next round.
   c. Otherwise, repeat s - 1 times: x = x^2 mod n. If x = n - 1, base passes; advance to next round. If x = 1, candidate is composite.
   d. If the square loop finishes without reaching n - 1, candidate is composite.
7. If candidate fails any round, discard candidate and return to Step 2.
8. If all k = 40 rounds pass, candidate n is confirmed as a probable prime.
9. Validate exact bit length: assert n.bit_length() == 512.
10. Execute multi-method independent primality verification:
    a. Small prime trial division for all primes p <= 2000.
    b. Fermat's Little Theorem test (a^(n-1) ≡ 1 mod n) across 10 independent bases {41, 43, 47, 53, 59, 61, 67, 71, 73, 79}.
    c. Strong Lucas Probable Prime test (Baillie–PSW) using Selfridge parameter Method A.
11. Output the validated 512-bit probable prime in decimal and hexadecimal along with experimental metrics.
Flowchart
Start
  ↓
Set Assigned Bit Length = 512, Rounds k = 40
  ↓
Generate Random 512-bit Integer
  ↓
Set MSB (Bit 511 = 1) & LSB (Bit 0 = 1)
  ↓
Trial Division Pre-filter (Primes ≤ 1000)
  ↓
Divisible by Small Prime? ──(Yes)──→ Discard Candidate & Regenerate
  ↓ (No)                                      ↑
Decompose n - 1 = 2^s · d (d is odd)          │
  ↓                                           │
Select Base a (Deterministic / Random)        │
  ↓                                           │
Compute x = a^d mod n                         │
  ↓                                           │
x == 1 or x == n - 1? ──(Yes)──→ Next Round   │
  ↓ (No)                                      │
Square Loop: Repeat r from 1 to s - 1         │
  ↓                                           │
x = x^2 mod n                                 │
  ↓                                           │
x == n - 1? ──(Yes)────────────→ Next Round   │
  ↓ (No)                                      │
x == 1 or Loop Finishes? ──(Yes)──────────────┘ (Composite Witness)
  ↓ (All k Rounds Passed)
Probable Prime Identified!
  ↓
Validate Exact Bit Length (bit_length == 512)
  ↓
Multi-Method Independent Primality Verification
(Trial Division ≤ 2000, 10-Base Fermat Test, Strong Lucas / Baillie–PSW)
  ↓
Log Results & Format Experimental Table
  ↓
Output Verified 512-bit Prime
  ↓
End

Important Commands
mkdir -p classical/miller_rabin/{outputs,testcases}

python3 classical/miller_rabin/main.py
python3 -m unittest classical/miller_rabin/testcases/test_miller_rabin.py

cat classical/miller_rabin/outputs/result.txt

Observations
- Assigned bit length: 512 bits.
- Generated prime candidate (Decimal): 13023594972312266040416825252540092750415079615322394682065789011411950572427481184800045125067557293193280200765540668122592380336658495230667383438447781.
- Generated prime candidate (Hex): 0xf8aa019536653a3bede40c5e4dc23a38f3b6d374e9f44101201dd6ce115a4775a69a347ab15f913952a70cfacd8c69489ba444f0d41fd22afd0d253decba14a5.
- Actual bit length: Exactly 512 bits verified (2^511 <= n < 2^512, MSB bit 511 = 1, LSB bit 0 = 1).
- Total candidates tested: 123 odd integers (pre-filter eliminated non-primes rapidly; only candidates passing small-prime checks were subjected to Miller–Rabin rounds).
- Number of Miller–Rabin rounds executed: 40 rounds (error probability <= 2^-80 ≈ 8.27 × 10^-25).
- Candidate factorization: (n - 1) = 2^2 · d, where power of two s = 2 and d is a 510-bit odd integer.
- Miller–Rabin deterministic base verification: Successfully passed all specified bases [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
  - Bases 5, 11, 13, 19, 31 passed at initial test (a^d ≡ 1 or n - 1 mod n).
  - Bases 2, 3, 7, 17, 23, 29, 37 passed at square step 1 (a^(d*2^1) ≡ n - 1 mod n).
- Multi-method independent verification:
  - Small prime trial division: Passed (no factors <= 2000).
  - Fermat's Little Theorem test: Passed across 10 independent bases {41, 43, 47, 53, 59, 61, 67, 71, 73, 79} (a^(n-1) ≡ 1 mod n).
  - Strong Lucas Probable Prime test (Baillie–PSW): Passed using Selfridge Parameter Method A (zero known counterexamples).
- Total prime generation and verification execution time: 0.0272 seconds.
- Test suite execution: All 8 unit tests in testcases/test_miller_rabin.py passed in 0.035 seconds.
