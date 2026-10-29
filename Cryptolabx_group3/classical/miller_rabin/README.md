# Cryptographic Prime Generation Using Miller–Rabin

## 1. Objective
Generate a probable prime of **512-bit length** using the Miller–Rabin primality test, implement pre-filtering optimizations, perform comprehensive verification against specified bases and independent primality-testing algorithms, and log experimental results in a structured format.

---

## 2. Directory Structure

```text
classical/miller_rabin/
├── __init__.py                     # Package initialization
├── miller_rabin.py                 # Core primality testing, candidate generation, and verifications
├── main.py                         # Main execution script and results logger
├── README.md                       # Complete technical documentation
├── outputs/
│   └── result.txt                  # Output logs and formatted experimental results table
└── testcases/
    ├── __init__.py
    └── test_miller_rabin.py        # Comprehensive unit tests
```

---

## 3. Mathematical Background

### 3.1 Why Miller–Rabin?
Direct trial division for a 512-bit integer is computationally infeasible since $2^{256} \approx 1.15 \times 10^{77}$ operations would be needed in the worst case. Fermat's Little Theorem states that if $n$ is prime, then for any $a$ coprime to $n$:

$$a^{n-1} \equiv 1 \pmod n$$

However, composite numbers known as **Carmichael numbers** (e.g., $561, 1105, 1729$) satisfy Fermat's equation for all coprime bases, making Fermat's test alone insufficient.

The **Miller–Rabin test** overcomes this by testing non-trivial square roots of $1$ modulo $n$. In any prime field $\mathbb{Z}_p$, the only solutions to $x^2 \equiv 1 \pmod p$ are $x \equiv 1$ and $x \equiv -1 \pmod p$. If any other square root of 1 is discovered during repeated squaring, $n$ is guaranteed to be composite.

### 3.2 Algorithm Formulation
Given an odd candidate integer $n > 3$:
1. Write $n - 1$ as:
   $$n - 1 = 2^s \cdot d \quad \text{where } d \text{ is odd, } s \ge 1$$
2. For a chosen base $a \in [2, n - 2]$:
   - Compute $x_0 = a^d \pmod n$.
   - If $x_0 = 1$ or $x_0 = n - 1$, then $n$ passes this round.
   - Otherwise, compute successive squarings:
     $$x_r = x_{r-1}^2 \pmod n \quad \text{for } r = 1, 2, \dots, s - 1$$
   - If for some $r$, $x_r = n - 1$, then $n$ passes this round.
   - If $x_r = 1$ before reaching $n - 1$, a non-trivial square root of 1 is found, so $n$ is **composite**.
   - If the sequence ends without encountering $n - 1$, then by Fermat's theorem $a^{n-1} \not\equiv 1 \pmod n$, so $n$ is **composite**.

### 3.3 Error Probability
For any odd composite $n$, the number of bases $a \in [2, n-2]$ that falsely witness $n$ as prime is at most $\frac{1}{4}(n-1)$.
Performing $k$ independent rounds with randomly selected bases yields an error probability:

$$P(\text{composite passes } k \text{ rounds}) \le \left(\frac{1}{4}\right)^k = 2^{-2k}$$

For $k = 40$:
$$P \le 2^{-80} \approx 8.27 \times 10^{-25}$$
This is well within cryptographic security requirements (FIPS 186-4).

---

## 4. Implementation Steps

1. **Candidate Generation**:
   - Cryptographically secure random 512-bit integer generated with `secrets.randbits(512)`.
   - Bit 511 (MSB) forced to `1` ($n \ge 2^{511}$) ensuring exact 512-bit length.
   - Bit 0 (LSB) forced to `1` ensuring $n$ is odd.

2. **Pre-filtering Optimization**:
   - Trial division against small primes up to $1000$ (168 primes) eliminates $\sim 90\%$ of composite numbers instantly, reducing costly modular exponentiations.

3. **Miller–Rabin Multi-round Testing**:
   - Tests deterministic small bases ($2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37$) followed by random bases up to $k = 40$ rounds.

4. **Independent Verifications**:
   - **Bit Length Demonstration**: Verify $n.bit\_length() == 512$ and $2^{511} \le n < 2^{512}$.
   - **Specified Bases Check**: Detailed round-by-round log for specific bases.
   - **Small Prime Trial Division**: Ensure no prime factor $\le 2000$.
   - **Fermat's Primality Test**: Verify $a^{n-1} \equiv 1 \pmod n$ for 10 independent prime bases.
   - **Strong Lucas Primality Test (Baillie-PSW)**: Selfridge parameter method A Lucas test. Combined with Miller-Rabin base 2, forms the Baillie-PSW primality test which has zero known counterexamples.

---

## 5. Execution

### Run Prime Generation and Verification
```bash
python3 main.py
```

### Run Unit Tests
```bash
python3 -m unittest testcases/test_miller_rabin.py
```
