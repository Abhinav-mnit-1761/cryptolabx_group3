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
├── classical/              # Classical cryptography algorithms
├── attacks/                # Cryptanalysis and attack modules
├── math/                   # Mathematical utilities
├── modern/                 # Modern cryptographic algorithms
├── analysis/               # Analysis utilities
│   └── file_analysis.py
├── datasets/               # Sample and future datasets
├── docs/                   # Project documentation
├── tests/                  # Test programs
│   └── vulnerable.py       # SAST testing program
├── utils/                  # Utility modules
│   └── logger.py
├── outputs/                # Program output and logs
├── main.py                 # Main command-line interface
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
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

The `datasets/` directory contains sample text files that can be used for current and future cryptography and cryptanalysis experiments.

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
- Git
- GitHub
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

### 4. Select an option from the menu

Follow the instructions displayed by the command-line interface.

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

The virtual environment is excluded from version control using `.gitignore`.

---

## Future Modules

The following modules are planned for future laboratory assignments:

### Classical Cryptography

- Caesar Cipher
- Vigenère Cipher
- Playfair Cipher
- Hill Cipher

### Modern Cryptography

- AES
- DES
- RSA
- Hashing Algorithms

### Cryptanalysis

- Frequency Analysis
- Brute-Force Attacks
- Cryptanalysis Tools

Additional datasets, algorithms, tests, and utilities will be added as the laboratory work progresses.

---
### Assigned Application: Hospital Management System
## Core Functions
Manage patient registration, appointments, prescriptions, billing, and medical records

### Lab Progress
## vulnerabilites added
SQL Injection
Broken Access Control
File Upload vulnerability

## Version Control

Git is used for version control and GitHub is used to host the project repository.

Repository:

https://github.com/Abhinav-mnit-1761/cryptolabx_group3

---

## Author
**Abhinav Shankhwar**  
Roll Number: **2024ucp1761**

Prepared for the **Cryptography Laboratory (22CPP307)**.
