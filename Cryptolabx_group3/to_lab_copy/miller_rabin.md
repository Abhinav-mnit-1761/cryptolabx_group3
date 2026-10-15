# Laboratory Notebook — Cryptographic Prime Generation Using Miller–Rabin

## Aim
To generate a probable prime of 512-bit length using the Miller–Rabin primality test, verify that the generated number has exactly the assigned bit length, passes Miller–Rabin for specified bases, and independently verify the result using multiple independent primality tests (Fermat test, trial division, and Strong Lucas test).

---

## Brief Theory
Prime generation is fundamental to asymmetric cryptography, such as RSA, Diffie–Hellman, and DSA key generation. Deterministic prime generation or brute-force trial division for 512-bit numbers is computationally impossible because it requires factoring numbers on the order of $2^{256}$.

Instead, cryptographic systems generate random candidate integers and test them with probabilistic primality tests. Fermat's Little Theorem ($a^{n-1} \equiv 1 \pmod n$) is insufficient due to Carmichael numbers ($561, 1105, 1729$), which pass Fermat's test for all coprime bases despite being composite.

The **Miller–Rabin primality test** overcomes this by testing for non-trivial square roots of $1$ modulo $n$. For any odd integer $n > 3$, we factor $n - 1$ as $2^s \cdot d$ where $d$ is odd. For any base $a \in [2, n - 2]$:
1. Compute $x_0 = a^d \pmod n$. If $x_0 = 1$ or $x_0 = n - 1$, $n$ passes this round.
2. Otherwise, iteratively square $x_r = x_{r-1}^2 \pmod n$ for $r \in [1, s - 1]$. If $x_r = n - 1$, $n$ passes.
3. If $x_r = 1$ before $n - 1$ or the loop finishes without reaching $n - 1$, $n$ is composite.

For any composite number, at least $3/4$ of all bases witness its compositeness. Repeating the test with $k = 40$ independent rounds ensures an error probability $\le (1/4)^{40} = 2^{-80} < 10^{-24}$, satisfying cryptographic standards (FIPS 186-4).

---

## Algorithm and Flowchart

### Algorithm
1. **Input**: Assigned bit length $B = 512$, number of rounds $k = 40$.
2. **Generate Candidate**:
   - Sample 512 random bits.
   - Set Most Significant Bit (MSB, bit 511) to 1 to guarantee 512-bit length.
   - Set Least Significant Bit (LSB, bit 0) to 1 to guarantee an odd number.
3. **Pre-filter**: Check candidate divisibility against small primes ($\le 1000$). If divisible, reject candidate and go to Step 2.
4. **Decompose**: Factor $n - 1 = 2^s \cdot d$, with $d$ odd.
5. **Miller–Rabin Primality Test**:
   - For each base $a \in \{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37\} \cup \{\text{random bases}\}$:
     - Compute $x = a^d \pmod n$.
     - If $x == 1$ or $x == n - 1$, continue to next base.
     - Repeat $s - 1$ times: $x = x^2 \pmod n$. If $x == n - 1$, break and continue to next base; if $x == 1$, candidate is composite.
     - If loop completes without $x == n - 1$, candidate is composite.
   - If composite, reject and go to Step 2.
6. **Verification**:
   - Verify bit length: assert $n.bit\_length() == 512$.
   - Verify specific bases: demonstrate $a^d \pmod n$ and square stages for assigned bases.
   - Independent verification: run Fermat test on separate bases, trial division with primes up to 2000, and Strong Lucas (Baillie-PSW) test.
7. **Output**: Return validated 512-bit probable prime, execution metrics, and experimental table.

### Flowchart
```text
               Start
                 ↓
      Set Assigned Bit Length = 512
                 ↓
    Generate Random 512-bit Integer
        (Force MSB = 1, LSB = 1)
                 ↓
    Pre-filter: Trial Division by
        Small Primes (p ≤ 1000)
                 ↓
           Divisible?  ───────(Yes)─────→ [Reject Candidate]
                 ↓ (No)                            ↑
      Decompose: n - 1 = 2^s * d                   │
                 ↓                                 │
     Miller-Rabin Primality Test                   │
       (k = 40 Independent Rounds)                 │
                 ↓                                 │
         Candidate Composite? ─(Yes)───────────────┘
                 ↓ (No)
     Probable Prime Identified!
                 ↓
       Multi-Method Verification:
   1. Confirm Bit Length == 512
   2. Explicit Base Traces
   3. Independent Small Prime Check
   4. Independent Fermat Test (10 bases)
   5. Independent Strong Lucas Test
                 ↓
     Generate Experimental Table
     & Save Results to File
                 ↓
                End
```

---

## Important Commands
```bash
# Navigate to directory
cd classical/miller_rabin

# Run prime generation, verification and output table
python3 main.py

# Run unit tests
python3 -m unittest testcases/test_miller_rabin.py
```

---

## Experimental Results Template

| Parameter | Value |
|---|---|
| Assigned bit length | 512 |
| Generated prime candidate | *(512-bit decimal integer)* |
| Actual bit length of the candidate | 512 |
| Number of candidates tested | *(count, e.g. ~150–250)* |
| Number of Miller–Rabin rounds | 40 |
| Total execution time | *(seconds, e.g. ~0.2–0.6s)* |

---

## Verification Summary
- **Exact Bit Length**: Verified $2^{511} \le n < 2^{512}$, confirming bit length is exactly 512 bits.
- **Miller–Rabin on Specified Bases**: Passed for deterministic bases $a \in \{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37\}$.
- **Independent Primality Verification**:
  1. No factors found in trial division up to $2000$.
  2. Fermat's test ($a^{n-1} \equiv 1 \pmod n$) passed on 10 independent bases $\{41, 43, 47, 53, 59, 61, 67, 71, 73, 79\}$.
  3. Strong Lucas test (Baillie-PSW test) passed with Selfridge parameter method A.
