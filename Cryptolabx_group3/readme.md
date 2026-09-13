# CryptoLabX

## Project Overview

CryptoLabX is a modular cryptography toolkit developed as part of the Cryptography Laboratory course (22CPP307).

The project is designed as a reusable framework that will gradually include classical cryptographic algorithms, modern cryptographic algorithms, cryptanalysis techniques, file-analysis utilities, datasets, and supporting tools.

The project follows a modular structure so that new algorithms and analysis techniques can be added independently in future laboratory assignments.

---

## Team Members

| Name              | Roll Number |
| ----------------- | ----------- |
| Abhinav Shankhwar | 2024ucp1761  |

---

## Project Structure

```text
CryptoLabX_Group3/
│
├── classical/                  # Classical cryptography algorithms
│   └── monoalphabetic/         # Monoalphabetic substitution cipher
├── attacks/                    # Cryptanalysis and attack modules
│   ├── shift_cipher_attack/    # Shift cipher cryptanalysis (brute-force & chi-square)
│   └── vigenere_attack/        # Vigenère cipher cryptanalysis (Kasiski & IoC)
│       ├── vigenere.py         # Core cipher algorithms and attack functions
│       ├── main.py             # Automated cryptanalysis pipeline
│       └── outputs/            # Output logs and recovered plaintext
├── datasets/                   # Sample datasets and ciphertexts
│   └── plaintext_veg.txt       # Vigenère ciphertext dataset
├── secure_applications/        # Hospital Management System security lab
├── analysis/                   # Analysis utilities
│   └── file_analysis.py
├── docs/                       # Project documentation
├── tests/                      # Test programs
│   └── vulnerable.py           # SAST testing program
├── utils/                      # Utility modules
│   └── logger.py
├── outputs/                    # Program output and logs
├── main.py                     # Main command-line interface
├── readme.md                   # Project documentation
└── requirements.txt            # Python dependencies
```

---

## Features Implemented

### Command-Line Interface

CryptoLabX provides a menu-driven command-line interface with options for:

- Encryption
- Decryption
- Attack
- File Analysis
- Exit

Features that are not yet implemented display an appropriate message.

### Vigenère Cipher Cryptanalysis

An automated cryptanalysis framework for breaking polyalphabetic Vigenère ciphers using statistical and algebraic techniques:

1. **Ciphertext Preprocessing**: Normalizes ciphertext, removing non-alphabetic characters and standardizing case.
2. **Kasiski Examination**:
   - Scans ciphertext for repeated n-grams of lengths 3 to 5.
   - Calculates exact index distances between repeated occurrences.
   - Computes prime factor frequencies to derive candidate key lengths.
3. **Index of Coincidence (IoC)**:
   - Evaluates the Index of Coincidence across partitioned cosets for candidate key lengths:
     `IC = sum(f_i * (f_i - 1)) / (N * (N - 1))`
   - Identifies the true key length by locating peaks matching standard English text (approx. 0.065 to 0.068).
4. **Chi-Square Frequency Analysis**:
   - Splits ciphertext into $L$ independent cosets (where $L$ is key length), converting the polyalphabetic cipher into $L$ Caesar ciphers.
   - Tests all 26 possible shifts against standard English letter frequencies using Chi-Square goodness-of-fit:
     `Chi-Square Score = sum((Observed - Expected)^2 / Expected)`
   - Reconstructs the encryption key character by character.
5. **Decryption and Verification**:
   - Decrypts the ciphertext using modular arithmetic:
     `P[i] = (C[i] - K[i % L]) mod 26`
   - Automatically re-encrypts the decrypted plaintext and verifies matching with the original ciphertext.
   - Saves all findings to `attacks/vigenere_attack/outputs/result.txt`.

#### Lab Cryptanalysis Results:
- **Ciphertext Length**: 395 characters
- **Estimated Key Length**: `14` (Average IC = `0.0644`)
- **Recovered Key**: `AMBROISETHOMAS`
- **Decrypted Plaintext**: Aria from *Mignon* (*"DO YOU KNOW THE LAND WHERE THE ORANGE TREE BLOSSOMS..."*)
- **Verification Status**: `True` (Re-encryption verified)

### Shift Cipher Cryptanalysis

- **Brute-force dictionary attack**: Tests all 26 key possibilities against an English dictionary to score valid words.
- **Chi-Square frequency attack**: Calculates chi-square distribution against standard English frequencies to recover the shift key without a dictionary.

### Monoalphabetic Substitution Cipher

- Implementation of monoalphabetic substitution cipher in C++ with frequency cryptanalysis capabilities.

### File Analysis

The file analysis module provides:

- Character count
- Word count
- Line count
- Unique character count
- Letter frequency analysis

### Logging

The project includes an execution logging mechanism that records:

- Date and time
- Selected operation
- Execution details

### Dataset Support

The `datasets/` directory contains sample text files that can be used for cryptography and cryptanalysis experiments (e.g., `plaintext_veg.txt`).

### Static Application Security Testing

Semgrep is used to perform Static Application Security Testing (SAST) on Python source code.

The SAST experiment includes an intentionally vulnerable test program containing examples of insecure practices such as:

- Unsafe command execution using `shell=True`
- Weak MD5 password hashing
- Hardcoded credentials

Semgrep successfully identified security issues in the test program.

---

## Technologies Used

- Python 3
- C++
- Git & GitHub
- Visual Studio Code
- Ubuntu / WSL
- Semgrep

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Abhinav-mnit-1761/cryptolabx_group3.git
```

### 2. Navigate to the project

```bash
cd cryptolabx_group3/Cryptolabx_group3
```

### 3. Run the toolkit

```bash
python3 main.py
```

### 4. Run Vigenère Cryptanalysis Lab

```bash
cd attacks/vigenere_attack
python3 main.py
```
The attack will execute Kasiski examination, compute Index of Coincidence, deduce the 14-character key `AMBROISETHOMAS`, decrypt the ciphertext, verify the decryption, and save output to `outputs/result.txt`.

---

## Static Security Analysis

Semgrep can be installed in a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install semgrep
```

Check the installed version:

```bash
semgrep --version
```

Run Semgrep on the vulnerable test program:

```bash
semgrep scan tests/vulnerable.py
```

Run the security-audit rules:

```bash
semgrep scan --config=p/security-audit tests/vulnerable.py
```

---

## Assigned Application: Hospital Management System
### Core Functions
Manage patient registration, appointments, prescriptions, billing, and medical records.

### Vulnerabilities Analyzed & Demonstrated
- SQL Injection
- Broken Access Control
- File Upload Vulnerability

---

## Version Control

Git is used for version control and GitHub is used to host the project repository.

Repository:
https://github.com/Abhinav-mnit-1761/cryptolabx_group3

---

## Author
**Abhinav Shankhwar**  
Roll Number: **2024ucp1761**

Prepared for the **Cryptography Laboratory (22CPP307)**.