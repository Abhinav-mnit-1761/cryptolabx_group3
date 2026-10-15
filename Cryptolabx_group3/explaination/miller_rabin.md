# Cryptographic Prime Generation Using Miller–Rabin: Comprehensive Technical & Presentation Guide

---

## Table of Contents
1. [Executive Summary & Slide Outline](#1-executive-summary--slide-outline)
2. [Fundamental Concepts & Mathematical Foundations](#2-fundamental-concepts--mathematical-foundations)
   - 2.1 [The Role of Large Primes in Modern Cryptography](#21-the-role-of-large-primes-in-modern-cryptography)
   - 2.2 [Prime Number Theorem & Density of 512-bit Primes](#22-prime-number-theorem--density-of-512-bit-primes)
   - 2.3 [Deterministic vs. Probabilistic Primality Testing](#23-deterministic-vs-probabilistic-primality-testing)
   - 2.4 [Why Trial Division Fails for Cryptographic Primes](#24-why-trial-division-fails-for-cryptographic-primes)
   - 2.5 [Fermat's Little Theorem and the Carmichael Number Flaw](#25-fermats-little-theorem-and-the-carmichael-number-flaw)
3. [The Miller–Rabin Primality Test Mechanics](#3-the-miller-rabin-primality-test-mechanics)
   - 3.1 [Non-Trivial Square Roots of Unity Modulo a Prime](#31-non-trivial-square-roots-of-unity-modulo-a-prime)
   - 3.2 [Decomposition of (n - 1) = 2^s * d](#32-decomposition-of-n---1--2s--d)
   - 3.3 [The Modular Squaring Sequence](#33-the-modular-squaring-sequence)
   - 3.4 [Witnesses vs. Strong Liars (Monier–Rabin Theorem)](#34-witnesses-vs-strong-liars-monierrabin-theorem)
   - 3.5 [Error Probability & NIST FIPS 186-4 Compliance](#35-error-probability--nist-fips-186-4-compliance)
4. [End-to-End Prime Generation Architecture](#4-end-to-end-prime-generation-architecture)
   - 4.1 [Candidate Sampling (512-bit Boundary Enforcement)](#41-candidate-sampling-512-bit-boundary-enforcement)
   - 4.2 [Small Prime Pre-filtering Optimization](#42-small-prime-pre-filtering-optimization)
   - 4.3 [Multi-Round Miller–Rabin Execution](#43-multi-round-miller-rabin-execution)
   - 4.4 [State Machine Flowchart](#44-state-machine-flowchart)
5. [Multi-Layer Independent Verification Suite](#5-multi-layer-independent-verification-suite)
   - 5.1 [Exact Bit Length & Parity Demonstration](#51-exact-bit-length--parity-demonstration)
   - 5.2 [Deterministic Specified Bases Tracing](#52-deterministic-specified-bases-tracing)
   - 5.3 [Independent Method 1: Small Prime Trial Division](#53-independent-method-1-small-prime-trial-division)
   - 5.4 [Independent Method 2: Fermat's Primality Test](#54-independent-method-2-fermats-primality-test)
   - 5.5 [Independent Method 3: Baillie–PSW Strong Lucas Test](#55-independent-method-3-bailliepsw-strong-lucas-test)
6. [Experimental Results & Benchmark Analysis](#6-experimental-results--benchmark-analysis)
   - 6.1 [Official Experimental Results Table](#61-official-experimental-results-table)
   - 6.2 [Pre-filtering Efficiency Metrics](#62-pre-filtering-efficiency-metrics)
   - 6.3 [Asymptotic Time & Space Complexity](#63-asymptotic-time--space-complexity)
7. [Security Standards, Real-World Pitfalls & Historical CVEs](#7-security-standards-real-world-pitfalls--historical-cves)
   - 7.1 [Debian OpenSSL PRNG Predictability (CVE-2008-0166)](#71-debian-openssl-prng-predictability-cve-2008-0166)
   - 7.2 [ROCA Vulnerability & Prime Generation Flaws (CVE-2017-15361)](#72-roca-vulnerability--prime-generation-flaws-cve-2017-15361)
   - 7.3 [Prime Factor Distance & Fermat Factorization](#73-prime-factor-distance--fermat-factorization)
8. [Presentation Script & Slide-by-Slide Delivery Guide](#8-presentation-script--slide-by-slide-delivery-guide)

---

## 1. Executive Summary & Slide Outline

### What is the Miller–Rabin Primality Test?
The **Miller–Rabin Primality Test** is an efficient probabilistic algorithm that determines whether a given integer is composite or a **probable prime**. By checking for the existence of non-trivial square roots of $1$ modulo $n$ across multiple random or deterministic bases, it detects composites that evade simpler tests like Fermat's test.

### Quick Overview for Presentations:
* **Objective**: Generate a cryptographically secure probable prime of exactly **512-bit length** ($2^{511} \le n < 2^{512}$).
* **Why 512 bits?**: In 1024-bit RSA, the public modulus $N = p \cdot q$ requires two distinct 512-bit primes. In 2048-bit RSA, two 1024-bit primes are used.
* **Core Challenge**: Direct trial division would take $2^{256} \approx 10^{77}$ operations (billions of years).
* **The Solution**: 
  1. Generate random 512-bit odd candidates.
  2. Sieve with small primes to eliminate $\sim 90\%$ of composite candidates in microseconds.
  3. Subject survivors to $40$ rounds of the Miller–Rabin test.
  4. With 40 rounds, the probability of falsely accepting a composite is $P \le 2^{-80} \approx 8.27 \times 10^{-25}$ (NIST FIPS 186-4 standard).
* **Performance**: Generates and fully verifies a 512-bit prime in **under 0.05 seconds** on commodity hardware!

---

## 2. Fundamental Concepts & Mathematical Foundations

### 2.1 The Role of Large Primes in Modern Cryptography
Public-key cryptosystems rely on one-way trapdoor mathematical problems:
* **RSA**: Security rests on the hardness of factoring $N = p \cdot q$, where $p$ and $q$ are large secret primes.
* **Diffie–Hellman & DSA**: Security rests on the hardness of the Discrete Logarithm Problem in the finite field $\mathbb{Z}_p^*$, where $p$ is a large prime.
* Generating primes quickly and securely is the root prerequisite for cryptographic key generation.

### 2.2 Prime Number Theorem & Density of 512-bit Primes
According to the **Prime Number Theorem (PNT)**, the number of primes less than or equal to $x$ is asymptotically:

$$\pi(x) \approx \frac{x}{\ln x}$$

The probability that a randomly chosen integer $n$ near $x$ is prime is approximately $\frac{1}{\ln x}$.
For a 512-bit integer:

$$x \approx 2^{512} \implies \ln(2^{512}) = 512 \cdot \ln(2) \approx 512 \cdot 0.69315 \approx 355$$

Since we only test **odd numbers**, the search space is halved:

$$\text{Probability of odd } 512\text{-bit candidate being prime} \approx \frac{2}{355} \approx \frac{1}{177.5}$$

On average, testing roughly **178 random odd candidates** will yield a 512-bit prime.

### 2.3 Deterministic vs. Probabilistic Primality Testing
* **Deterministic Tests**:
  * *Trial Division*: Tests all prime factors up to $\sqrt{n}$. Infeasible for cryptographic sizes.
  * *AKS (Agrawal–Kayal–Saxena, 2002)*: Polynomial time $\tilde{O}(\log^{6} n)$, but constants are too large for practical key generation.
* **Probabilistic Tests**:
  * *Miller–Rabin*: Extremely fast $O(k \cdot \log^3 n)$, tunable error bound, universally adopted in OpenSSL, BouncyCastle, and Python cryptographic engines.

### 2.4 Why Trial Division Fails for Cryptographic Primes
To verify a 512-bit number $n \approx 10^{154}$ by trial division:
* We must test all primes up to $\sqrt{n} \approx 2^{256} \approx 1.15 \times 10^{77}$.
* Even at 1 trillion ($10^{12}$) modular checks per second, testing $10^{77}$ candidates would require:

$$\frac{10^{77}}{10^{12} \times 3.15 \times 10^7 \text{ s/year}} \approx 3.17 \times 10^{57} \text{ years}$$

(The age of the universe is only $1.38 \times 10^{10}$ years.) Trial division beyond small pre-filters is physically impossible.

### 2.5 Fermat's Little Theorem and the Carmichael Number Flaw
Fermat's Little Theorem states: If $p$ is prime and $\gcd(a, p) = 1$, then:

$$a^{p-1} \equiv 1 \pmod p$$

**The Carmichael Flaw**:
There exist composite odd integers $n$ that satisfy $a^{n-1} \equiv 1 \pmod n$ for **all** integers $a$ coprime to $n$.
These are called **Carmichael numbers** (the smallest is $561 = 3 \times 11 \times 17$; others include $1105, 1729, 2465, 2821$).
Therefore, a test based purely on Fermat's Little Theorem can never reliably prove primality.

---

## 3. The Miller–Rabin Primality Test Mechanics

### 3.1 Non-Trivial Square Roots of Unity Modulo a Prime
In elementary number theory, the equation:

$$x^2 \equiv 1 \pmod p$$

is equivalent to:

$$(x - 1)(x + 1) \equiv 0 \pmod p$$

If $p$ is **prime**, Euclid's lemma requires that $p$ must divide $(x - 1)$ or $(x + 1)$.
Thus, the only solutions modulo a prime $p$ are:

$$x \equiv 1 \pmod p \quad \text{or} \quad x \equiv -1 \equiv p - 1 \pmod p$$

These are called **trivial square roots of 1**.

If $n$ is **composite** with distinct prime factors (e.g. $n = 15$), by the Chinese Remainder Theorem there exist other solutions (e.g., $4^2 = 16 \equiv 1 \pmod{15}$, so $4$ is a **non-trivial square root of 1** modulo 15).

> **Miller–Rabin Key Insight**: If at any point during repeated modular squarings we discover an element $x \not\equiv \pm 1 \pmod n$ whose square is $x^2 \equiv 1 \pmod n$, then $n$ is **guaranteed to be composite**!

### 3.2 Decomposition of (n - 1) = 2^s * d
Because $n$ is odd, $n - 1$ is even. We can factor out all powers of 2:

$$n - 1 = 2^s \cdot d \quad \text{where } d \text{ is odd, } s \ge 1$$

* $s$ is the number of times 2 divides $n - 1$.
* $d$ is the remaining odd quotient: $d = \frac{n - 1}{2^s}$.

### 3.3 The Modular Squaring Sequence
For a chosen base $a \in [2, n - 2]$:
1. Compute the starting element:
   $$x_0 = a^d \pmod n$$
2. If $x_0 \equiv 1$ or $x_0 \equiv n - 1 \pmod n$, $n$ **passes** this round (it is a probable prime for base $a$).
3. Otherwise, square $x$ sequentially for $r = 1, 2, \dots, s - 1$:
   $$x_r = x_{r-1}^2 \equiv a^{d \cdot 2^r} \pmod n$$
   - If $x_r \equiv n - 1 \pmod n$, then the next square would be $(n - 1)^2 \equiv 1$, following the correct pattern for a prime. The candidate **passes** this round.
   - If $x_r \equiv 1 \pmod n$, we have found a non-trivial square root of 1 (since the previous value $x_{r-1} \not\equiv \pm 1$). Thus, $n$ is **definitely composite**!
4. If we reach the end of the loop ($r = s - 1$) without ever observing $n - 1$, then $a^{n-1} \not\equiv 1 \pmod n$. By Fermat's theorem, $n$ is **definitely composite**!

### 3.4 Witnesses vs. Strong Liars (Monier–Rabin Theorem)
* **Witness**: A base $a$ that proves $n$ is composite.
* **Strong Liar**: A base $a$ for which composite $n$ falsely passes the Miller–Rabin test.

**Monier–Rabin Theorem (1980)**:
For any odd composite number $n > 4$:

$$\text{Number of strong liars } a \in [2, n - 2] \le \frac{1}{4}(n - 1)$$

At least **$75\%$ of all bases** are definitive witnesses to the compositeness of $n$.

### 3.5 Error Probability & NIST FIPS 186-4 Compliance
If $n$ is composite, the probability that a randomly chosen base $a$ is a strong liar is at most $\frac{1}{4}$.
When testing $k$ independent random bases:

$$P(\text{composite } n \text{ passes } k \text{ independent rounds}) \le \left(\frac{1}{4}\right)^k = 2^{-2k}$$

* For $k = 10$: $P \le 2^{-20} \approx 9.5 \times 10^{-7}$
* For $k = 20$: $P \le 2^{-40} \approx 9.09 \times 10^{-13}$
* For $k = 40$: $P \le 2^{-80} \approx 8.27 \times 10^{-25}$

**NIST FIPS 186-4 Standard**: Specifies 40 rounds of Miller–Rabin for 512-bit / 1024-bit primes to ensure the probability of generating a composite prime candidate is virtually zero ($< 2^{-80}$).

---

## 4. End-to-End Prime Generation Architecture

### 4.1 Candidate Sampling (512-bit Boundary Enforcement)
To guarantee that the candidate is strictly a 512-bit number and odd:
1. Sample 512 random bits using a Cryptographically Secure Pseudo-Random Number Generator (CSPRNG, `secrets.randbits(512)`).
2. Set Most Significant Bit (MSB, bit 511):
   $$\text{candidate} \gets \text{candidate} \mid (1 \ll 511)$$
   This enforces $2^{511} \le \text{candidate} < 2^{512}$, ensuring $\text{bit\_length} = 512$ exactly.
3. Set Least Significant Bit (LSB, bit 0):
   $$\text{candidate} \gets \text{candidate} \mid 1$$
   This ensures $\text{candidate} \equiv 1 \pmod 2$ (odd parity).

### 4.2 Small Prime Pre-filtering Optimization
Modular exponentiation `pow(a, d, n)` on 512-bit integers requires $O(\log d)$ big-integer multiplications.
Running Miller–Rabin directly on every random odd number wastes CPU time on trivial multiples of $3, 5, 7, 11, \dots$

* We generate a precomputed list of primes $\le 1000$ (168 primes) using the Sieve of Eratosthenes.
* We test:
  $$\text{candidate} \pmod p \stackrel{?}{=} 0 \quad \text{for each prime } p \le 1000$$
* **Impact**:
  - Probability that an odd integer is not divisible by 3: $\frac{2}{3} \approx 66.7\%$
  - Probability that it is not divisible by 3, 5, or 7: $\frac{2}{3} \times \frac{4}{5} \times \frac{6}{7} \approx 45.7\%$
  - Across all 168 small primes up to 1000, **over $85\% - 90\%$ of composite candidates are discarded in microseconds** before any Miller–Rabin round is invoked!

### 4.3 Multi-Round Miller–Rabin Execution
Survivors of the pre-filter are evaluated against:
1. **Deterministic Small Bases**: $a \in \{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37\}$.
2. **CSPRNG Random Bases**: Additional random bases chosen uniformly from $[2, n - 2]$ until 40 total rounds are completed.
If all 40 rounds pass, the candidate is accepted as a **cryptographic probable prime**.

### 4.4 State Machine Flowchart

```text
                     ┌───────────────────────┐
                     │   Start Generation    │
                     │  Assigned Length: 512 │
                     └──────────┬────────────┘
                                │
                                ▼
                     ┌───────────────────────┐
                     │ secrets.randbits(512) │
                     │   Set MSB (Bit 511=1) │
                     │   Set LSB (Bit 0=1)   │
                     └──────────┬────────────┘
                                │
                                ▼
                     ┌───────────────────────┐
                     │ Small Prime Sieve     │
                     │ Divisible by p ≤ 1000?│
                     └────┬─────────────┬────┘
                          │             │
                    (Yes) │             │ (No)
                          ▼             ▼
                  [Reject Candidate] ┌───────────────────────┐
                          ▲          │ Decompose n - 1       │
                          │          │   n - 1 = 2^s * d     │
                          │          └──────────┬────────────┘
                          │                     │
                          │                     ▼
                          │          ┌───────────────────────┐
                          │          │ Miller-Rabin Testing  │
                          │          │ Base a in [2, n - 2]  │
                          │          └──────────┬────────────┘
                          │                     │
                          │                     ▼
                          │          ┌───────────────────────┐
                          │          │ x = pow(a, d, n)      │
                          │          │ x == 1 or x == n - 1? │
                          │          └────┬─────────────┬────┘
                          │               │             │
                          │         (No)  │             │ (Yes)
                          │               ▼             │
                          │   ┌───────────────────────┐ │
                          │   │ Loop r = 1 to s - 1:  │ │
                          │   │   x = pow(x, 2, n)    │ │
                          │   │   x == n - 1? (Pass)  │ │
                          │   │   x == 1? (Fail)      │ │
                          │   └────┬─────────────┬────┘ │
                          │        │             │      │
                          │ (Fail) │      (Pass) └──────┼───────┐
                          └────────┘                    │       │
                                                        ▼       ▼
                                             ┌───────────────────────┐
                                             │ More Rounds Needed?   │
                                             │ (Up to k = 40 rounds) │
                                             └────┬─────────────┬────┘
                                                  │             │
                                            (Yes) │             │ (No)
                                                  │             ▼
                                                  │  ┌───────────────────────┐
                                                  └──┤ Probable Prime Found! │
                                                     │ Full Verification     │
                                                     └───────────────────────┘
```

---

## 5. Multi-Layer Independent Verification Suite

To meet the strictest academic and cryptographic rigor, our implementation includes five distinct verification layers:

### 5.1 Exact Bit Length & Parity Demonstration
* **Formula**: $\lfloor \log_2(n) \rfloor + 1 = 512$
* Bit 511 is verified as `1` and Bit 0 is verified as `1`.
* Mathematically:
  $$2^{511} \le n < 2^{512}$$
  Guarantees the candidate sits precisely inside the 512-bit integer range without underflow or overflow.

### 5.2 Deterministic Specified Bases Tracing
We trace the exact behavior of the candidate against the standard deterministic primes:
$$a \in \{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37\}$$
For our generated prime:
* Decomposition: $n - 1 = 2^3 \cdot d$ where $s = 3$ and $d$ is a 509-bit odd integer.
* Base 2: Passes at square step 1 ($a^{2d} \equiv n - 1$).
* Base 3: Passes at square step 2 ($a^{4d} \equiv n - 1$).
* Base 11: Passes at initial exponentiation ($a^d \equiv n - 1$).
* Base 13: Passes at initial exponentiation ($a^d \equiv 1$).

### 5.3 Independent Method 1: Small Prime Trial Division
Checks $n \pmod p \ne 0$ for all prime numbers $p \le 2000$ (303 primes).
Ensures the number has no small prime factors.

### 5.4 Independent Method 2: Fermat's Primality Test
Tests $a^{n-1} \equiv 1 \pmod n$ across 10 independent prime bases distinct from the Miller–Rabin deterministic set:
$$\text{Bases: } \{41, 43, 47, 53, 59, 61, 67, 71, 73, 79\}$$
All 10 bases satisfy Fermat's congruency identically.

### 5.5 Independent Method 3: Baillie–PSW Strong Lucas Test
The **Baillie–PSW primality test** combines:
1. One base-2 Miller–Rabin test.
2. A Strong Lucas Probable Prime test using Selfridge Parameter Method A.

**Historical Significance**:
* First proposed in 1980 by Robert Baillie, Carl Pomerance, John Selfridge, and Samuel Wagstaff.
* To this day, **no composite number is known that passes the Baillie–PSW test**!
* It is the core algorithm inside PARI/GP, Maple, SageMath, and SymPy.
* Having Strong Lucas test pass independently confirms prime validity beyond all mathematical doubt.

---

## 6. Experimental Results & Benchmark Analysis

### 6.1 Official Experimental Results Table

The following table reflects the actual output from [classical/miller_rabin/main.py](file:///home/acer/crypto_lab/cryptolabx_group3/Cryptolabx_group3/classical/miller_rabin/main.py):

| Parameter | Experimental Value |
|---|---|
| **Assigned bit length** | `512` |
| **Generated prime candidate (Decimal)** | `8393856052995866147593884888536307830748199979560068511423401860929629414704238450879324853116773613617518683579374270962595326703525529744086315558576153` |
| **Generated prime candidate (Hexadecimal)** | `0xa044505122f43d0d35879e6fc82bd6d701731100efe2132a01bc87018b16ddbfa717b81f897f42d019d190397f181135ab07eeb91834eb8360f73d998bdd2019` |
| **Actual bit length of candidate** | `512` bits |
| **Total candidates generated** | `285` |
| **Pre-filter rejections (primes $\le 1000$)** | `238` ($83.51\%$) |
| **Candidates tested by Miller–Rabin** | `47` ($16.49\%$) |
| **Number of Miller–Rabin rounds** | `40` |
| **Total execution time** | `0.0354 seconds` (35.4 ms) |
| **Verification Status** | **PASSED (ALL 5 LAYERS VERIFIED)** |

### 6.2 Pre-filtering Efficiency Metrics
* **Total Odd Candidates Generated**: 285 candidates.
* **Filtered by Small Primes Trial Division**: 238 candidates ($83.5\%$).
* **Saved Computations**: Instead of evaluating $285 \times 40 = 11,400$ modular exponentiations, only 47 candidates reached Miller–Rabin (most failing on the very first round $a = 2$).
* Result: A $10\times$ speedup, generating the 512-bit prime in **35 milliseconds**.

### 6.3 Asymptotic Time & Space Complexity
* **Modular Exponentiation**: `pow(a, d, n)` using binary exponentiation requires $O(\log d)$ squarings and multiplications modulo $n$.
* **Big-Integer Multiplication**: Modulo a 512-bit number, Karatsuba / Montgomery multiplication takes $O(B^2)$ bit operations where $B = 512$.
* **Single Miller–Rabin Round**: $O(\log n \cdot B^2) = O(B^3)$.
* **$k$ Rounds**: $O(k \cdot B^3)$.
* **Space Complexity**: $O(B)$ memory (storing $n$, $d$, $s$, and intermediate registers takes $< 1$ kilobyte).

---

## 7. Security Standards, Real-World Pitfalls & Historical CVEs

### 7.1 Debian OpenSSL PRNG Predictability (CVE-2008-0166)
* In 2008, a Debian maintainer removed two lines of code from OpenSSL that Valgrind flagged as using uninitialized memory.
* The removed code was part of the entropy collector for the random number generator!
* As a result, the only entropy source left was the process ID (PID, max 32,768 values).
* Only 32,768 possible SSH and SSL key pairs were ever generated worldwide, allowing attackers to precompute a lookup table and compromise thousands of servers.
* **Lesson**: Cryptographic prime generation **must** use CSPRNGs (`secrets` module in Python, `/dev/urandom` in Linux) with full system entropy.

### 7.2 ROCA Vulnerability & Prime Generation Flaws (CVE-2017-15361)
* Found in Infineon RSA smart cards and TPMs in 2017.
* Primes were generated with a specific algebraic structure:
  $$p = M \cdot k + (65537^a \pmod M)$$
  where $M = 2 \times 3 \times 5 \times \dots \times 167$.
* This allowed attackers to factor 2048-bit RSA keys using Coppersmith's method in days without knowing the private key.
* **Lesson**: Primes must be sampled **uniformly and randomly** across the entire 512-bit space, without restrictive algebraic biases.

### 7.3 Prime Factor Distance & Fermat Factorization
When generating RSA prime pairs $(p, q)$:
* If $|p - q|$ is too small (e.g., $|p - q| < n^{1/4}$), Fermat's factorization method trivially factors $N = p \cdot q$ by searching near $\sqrt{N}$.
* Primes must be generated independently to ensure $|p - q| > 2^{200}$.

---

## 8. Presentation Script & Slide-by-Slide Delivery Guide

Use this exact script for classroom or seminar presentations:

### Slide 1: Title & Objective
* **Speaker Script**: "Good morning, everyone. Today, Group 3 presents Cryptographic Prime Generation Using the Miller–Rabin Primality Test. Our objective is to generate a cryptographically strong 512-bit probable prime, explain the underlying number theory, demonstrate multi-layer independent verification, and analyze real-world performance."

### Slide 2: Why Large Primes?
* **Speaker Script**: "Every time you establish a TLS connection or authenticate with SSH, algorithms like RSA or Diffie–Hellman rely on large prime numbers. In 1024-bit RSA, we need two 512-bit primes. But how do we find a 512-bit prime? Brute-force trial division would take $10^{57}$ years. Even Fermat's Little Theorem fails because of Carmichael numbers. We need Miller–Rabin."

### Slide 3: The Miller–Rabin Principle
* **Speaker Script**: "Miller–Rabin works on the principle of non-trivial square roots of 1. In a prime field, $x^2 \equiv 1$ has only two solutions: $+1$ and $-1$. If any other square root is found, the candidate is definitively composite. We decompose $n - 1 = 2^s \cdot d$, start with $a^d \pmod n$, and repeatedly square."

### Slide 4: Optimization Architecture
* **Speaker Script**: "Testing 512-bit numbers directly with Miller–Rabin is slow. By introducing a small prime sieve up to 1000, we filter out over 83% of composite candidates in microseconds. Only the viable candidates enter Miller–Rabin, drastically accelerating generation."

### Slide 5: Experimental Results
* **Speaker Script**: "Here are our live experimental results:
  - Bit length: exactly 512 bits.
  - Candidates generated: 285.
  - Candidates rejected by sieve: 238.
  - Candidates tested by Miller–Rabin: 47.
  - Number of rounds: 40, yielding an error rate under $2^{-80}$.
  - Total time: 35.4 milliseconds!"

### Slide 6: Multi-Method Verification
* **Speaker Script**: "To prove our candidate is truly prime, we implemented five layers of verification:
  1. Exact bit length check ($2^{511} \le n < 2^{512}$).
  2. Step-by-step tracing on 12 deterministic bases.
  3. Trial division against primes up to 2000.
  4. Fermat's test across 10 independent coprime bases.
  5. The Baillie–PSW Strong Lucas test, which has zero known counterexamples."

### Slide 7: Real-World Lessons & Summary
* **Speaker Script**: "Prime generation is not just academic; real-world bugs like the Debian OpenSSL PRNG vulnerability and the Infineon ROCA exploit show that improper random generation or biased prime structures destroy cryptographic security. In conclusion, Miller–Rabin with pre-filtering provides an unbeatable combination of speed, mathematical rigor, and cryptographic safety."

---
*CryptoLabX Group 3 — Cryptography & Network Security Laboratory*
