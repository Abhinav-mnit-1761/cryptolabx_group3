# EXPERIMENT NO: 07
# TOPIC: AES-CBC PADDING ORACLE ATTACK

================================================================================
LABORATORY NOTEBOOK RECORD (HANDWRITTEN GUIDE)
================================================================================
Subject: Cryptography & Network Security Laboratory
Experiment: Assignment 07 - Padding Oracle Attack on AES-CBC
Target Copy Size: 4 to 5 Pages (Handwritten format)

--------------------------------------------------------------------------------
[PAGE 1: AIM, BRIEF THEORY, AND MATHEMATICAL FOUNDATION]
--------------------------------------------------------------------------------

1. AIM
------
To implement and analyze the Padding Oracle Attack on AES-128 in Cipher Block 
Chaining (CBC) mode with PKCS#7 padding, demonstrating how an attacker can 
recover the complete plaintext without knowledge of the secret key by exploiting 
side-channel padding validation oracle responses.


2. BRIEF THEORY (5-10 LINES)
----------------------------
AES-CBC mode decrypts ciphertext blocks using the equation:
    P_i = D_K(C_i) XOR C_{i-1}
where D_K(C_i) is the block cipher intermediate state I_i, and C_0 is the IV. 
PKCS#7 padding ensures data fits 16-byte block boundaries by appending N bytes 
of value N (e.g., 0x01, or 0x02 0x02). If a server reveals whether decrypted 
data has valid padding (through error codes, responses, or execution timing), 
it functions as a "Padding Oracle." Because the attacker controls the preceding 
block C_{i-1}, bitwise XOR enables direct manipulation of the decrypted plaintext 
P_i byte-by-byte. Iteratively querying the oracle with crafted candidate bytes 
allows the attacker to deduce the intermediate state I_i and recover original 
plaintext without attacking the 128-bit AES key.


3. MATHEMATICAL FOUNDATION & WORKING PRINCIPLE
----------------------------------------------
The vulnerability stems from the malleability of the CBC decryption operation:
    P_i = D_K(C_i) XOR C_{i-1}

Define the intermediate decryption state as:
    I_i = D_K(C_i)   [Fixed for a given ciphertext block C_i and key K]

Therefore:
    P_i = I_i XOR C_{i-1}

When the attacker submits a forged previous block C'_{i-1} with target block C_i:
    P'_i = I_i XOR C'_{i-1}

Because XOR is a bitwise linear, independent operation:
    P'_i[k] = I_i[k] XOR C'_{i-1}[k]

The attacker does NOT know I_i or secret key K, but possesses 1-to-1 mathematical 
control over decrypted byte P'_i[k].

* PKCS#7 Padding Rules (Block Size = 16 bytes):
  - 1 byte padding needed:   0x01
  - 2 bytes padding needed:  0x02 0x02
  - 3 bytes padding needed:  0x03 0x03 0x03
  - 4 bytes padding needed:  0x04 0x04 0x04 0x04
  - 16 bytes padding needed: 0x10 0x10 ... (16 times)


--------------------------------------------------------------------------------
[PAGE 2: ATTACK MECHANICS & STEP-BY-STEP ALGORITHM]
--------------------------------------------------------------------------------

4. BYTE-BY-BYTE RECOVERY MECHANICS (RIGHT-TO-LEFT)
--------------------------------------------------
Plaintext recovery proceeds backwards from the last byte (k = 15) to byte (k = 0).

Step 1: Finding Byte 15 (Target Pad = 0x01)
  - Attacker sets C'_{i-1}[0..14] to 0x00.
  - Attacker iterates candidate byte g in [0, 255] for C'_{i-1}[15].
  - Submits probe (C'_{i-1}, C_i) to Oracle.
  - When Oracle returns True (Valid Padding), P'_i[15] must equal 0x01:
        P'_i[15] = I_i[15] XOR g = 0x01
        => I_i[15] = g XOR 0x01
  - The secret original plaintext byte is recovered:
        P_i[15] = I_i[15] XOR C_{i-1}[15]

Step 2: Disambiguation (False-Positive Protection for Pad 0x01)
  - If original decrypted byte at index 14 accidentally equaled 0x02, the oracle 
    might return True because of a 2-byte pad (0x02 0x02) rather than 0x01.
  - Disambiguation check: Invert byte 14: C'_{i-1}[14] ^= 0x01.
  - If Oracle STILL returns True, the pad is confirmed to be 0x01.
  - If Oracle returns False, discard g and continue searching.

Step 3: Generalizing to Byte k (for k = 14 down to 0)
  - Target pad value: pad = 16 - k (e.g., pad=0x02 for k=14; pad=0x03 for k=13).
  - For all known positions j > k:
        Force P'_i[j] = pad by setting: C'_{i-1}[j] = I_i[j] XOR pad
  - For unknown position k:
        Iterate candidate byte g in [0, 255]:
        Set C'_{i-1}[k] = g
        Query Oracle(C'_{i-1}, C_i)
        If True:
            I_i[k] = g XOR pad
            P_i[k] = I_i[k] XOR C_{i-1}[k]
            Break candidate search and proceed to byte k - 1.


5. STEP-BY-STEP ALGORITHM (NO COMPLETE SOURCE CODE)
---------------------------------------------------
ALGORITHM 1: RECOVER_BLOCK(Oracle, C_{i-1}, C_i, BlockSize=16)
Input:  Padding Oracle, previous block C_{i-1} (or IV), target block C_i
Output: Recovered plaintext block P_i, intermediate state I_i

1. Initialize bytearrays Intermediate[0..15] = 0, Plaintext[0..15] = 0.
2. For byte index k from 15 down to 0:
     a. Set target_pad = 16 - k.
     b. Initialize probe block C' of 16 bytes with zeros.
     c. For each known index j from (k + 1) to 15:
            C'[j] = Intermediate[j] XOR target_pad
     d. For candidate guess g from 0 to 255:
            C'[k] = g
            Send (C', C_i) to Oracle.
            If Oracle returns TRUE:
                If k == 15:  // Check for false positive
                    C'_check = copy(C')
                    C'_check[14] = C'_check[14] XOR 0x01
                    If Oracle(C'_check, C_i) is FALSE:
                        Continue candidate loop
                Intermediate[k] = g XOR target_pad
                Plaintext[k]    = Intermediate[k] XOR C_{i-1}[k]
                Break candidate loop
3. Return (Plaintext, Intermediate).

ALGORITHM 2: PADDING_ORACLE_ATTACK(Oracle, IV, Ciphertext)
Input:  Oracle, IV (16 bytes), Ciphertext blocks (C_1, C_2, ... C_M)
Output: Fully decrypted original plaintext message

1. Partition Ciphertext into 16-byte blocks: [C_1, C_2, ..., C_M].
2. Set C_0 = IV.
3. For block index i from 1 to M:
     (P_i, I_i) = RECOVER_BLOCK(Oracle, C_{i-1}, C_i)
     Concatenate P_i to FullPlaintext.
4. Validate and strip PKCS#7 padding from FullPlaintext.
5. Return the recovered plaintext string.


--------------------------------------------------------------------------------
[PAGE 3: FLOWCHART & IMPORTANT EXECUTION COMMANDS]
--------------------------------------------------------------------------------

6. FLOWCHART
-------------
           +---------------------------------------------+
           |                    START                    |
           +---------------------------------------------+
                                  |
                                  v
           +---------------------------------------------+
           | Receive (IV, C_1, C_2, ..., C_M) from Server |
           | Initialize Block Index i = 1, C_0 = IV      |
           +---------------------------------------------+
                                  |
            +-------------------->|
            |                     v
            |      +------------------------------+
            |      | Select Target Block C_i      |
            |      | Set Byte Index k = 15        |
            |      +------------------------------+
            |                     |
            |       +------------>|
            |       |             v
            |       |  +------------------------------------+
            |       |  | Set target_pad = 16 - k            |
            |       |  | For j > k: C'[j] = I[j] ^ target_pad|
            |       |  | Initialize candidate guess g = 0   |
            |       |  +------------------------------------+
            |       |             |
            |       |   +-------->|
            |       |   |         v
            |       |   |  +--------------------------------+
            |       |   |  | Set C'[k] = g                  |
            |       |   |  | Query Oracle: IsPadValid(C',Ci)|
            |       |   |  +--------------------------------+
            |       |   |         |
            |       |   |         v
            |       |   |    /---------\
            |       |   |   /  Oracle   \       NO
            |       |   |  <   Returns   >------------+
            |       |   |   \  TRUE?    /             |
            |       |   |    \---------/              |
            |       |   |         | YES               |
            |       |   |         v                   |
            |       |   |  +--------------------+     |
            |       |   |  | If k=15: Check     |     |
            |       |   |  | Disambiguation     |     |
            |       |   |  +--------------------+     |
            |       |   |         |                   |
            |       |   |         v                   v
            |       |   |  +--------------------+  +--------+
            |       |   |  | I[k] = g ^ pad     |  | g = g+1|
            |       |   |  | P[k] = I[k]^C_{i-1}|  +--------+
            |       |   |  +--------------------+     |
            |       |   |         |                   |
            |       |   |         v                   |
            |       |   |      [Found]                +--> (Next g)
            |       |   |         |
            |       |   +---------+
            |       |             |
            |       |             v
            |       |      /-------------\
            |       |     /   k == 0 ?    \      NO (k = k - 1)
            |       +----<  (Block Done?)  >--------------------+
            |             \               /
            |              \-------------/
            |                     | YES
            |                     v
            |          Append P_i to Plaintext
            |                     |
            |                     v
            |              /-------------\
            |             /   i == M ?    \      NO (i = i + 1)
            +------------<  (All Done?)    >--------------------+
                          \               /
                           \-------------/
                                  | YES
                                  v
           +---------------------------------------------+
           | Strip PKCS#7 Padding from Plaintext Bytes   |
           | Output Verified Plaintext                   |
           +---------------------------------------------+
                                  |
                                  v
           +---------------------------------------------+
           |                     END                     |
           +---------------------------------------------+


7. IMPORTANT COMMANDS & EXECUTION STEPS
----------------------------------------
# Step 1: Navigate to repository root & activate virtual environment
$ cd /home/acer/crypto_lab/cryptolabx_group3/Cryptolabx_group3
$ source .venv/bin/activate

# Step 2: Run Default Demonstration Attack (Decodes Server Message)
$ python3 attacks/padding_oracle_attack/src/main.py --demo

# Step 3: Run Interactive Attack Menu (Select options 1-4)
$ python3 attacks/padding_oracle_attack/src/main.py

# Step 4: Run Automated Comprehensive Test Suite
$ python3 attacks/padding_oracle_attack/testcases/test_oracle.py

# Step 5: View Output Result Log
$ cat attacks/padding_oracle_attack/outputs/result.txt


--------------------------------------------------------------------------------
[PAGE 4: EXPERIMENTAL OBSERVATIONS & PERFORMANCE ANALYSIS]
--------------------------------------------------------------------------------

8. EXPERIMENTAL OBSERVATIONS
----------------------------
The attack was executed in a controlled lab test bench against an AES-128-CBC 
oracle configured with a randomized, hidden 128-bit key.

A. Ciphertext Metadata:
   - Target Plaintext:           "abhinavisgod"
   - IV (Hex):                   b332d68df081d2e1be12f3fbf99147db
   - Ciphertext (Hex):           adaeb0442e3ea6318e843de3edbc6614
   - Total Ciphertext Length:    16 bytes (1 Block)

B. Attack Execution & Plaintext Recovery:
   - Recovered Plaintext:        "abhinavisgod"
   - Recovered Plaintext (Hex):  616268696e61766973676f64
   - Inferred PKCS#7 Padding:    0x04 0x04 0x04 0x04 (4 padding bytes)
   - Verification Status:        SUCCESSFUL (Match with Original Plaintext)

C. Block-by-Block Analysis:
   ------------------------------------------------------------------------
   Block # | Plaintext (Hex)                  | Intermediate State I_i (Hex) | Queries
   ------------------------------------------------------------------------
   Block 1 | 616268696e61766973676f6404040404 | d250bee49ee0a488cd759c9ffd9543df | 2704
   ------------------------------------------------------------------------

D. Query Complexity & Performance Metrics:
   - Total Oracle Queries:       2,704 queries
   - Total Ciphertext Bytes:     16 bytes
   - Average Queries per Byte:   169.00 queries/byte
   - Execution Time:             1.044 seconds


9. COMPLEXITY COMPARISON: BRUTE-FORCE VS PADDING ORACLE
-------------------------------------------------------
+--------------------+-------------------------+-------------------------+
| Parameter          | Brute-Force Key Search  | Padding Oracle Attack   |
+--------------------+-------------------------+-------------------------+
| Target             | Secret 128-bit Key K    | Intermediate State I_i  |
| Mathematical Cost  | 2^128 operations        | <= 256 * 16 queries/blk |
| Worst-Case Queries | ~3.40 * 10^38 attempts  | 4,096 queries / block   |
| Average Queries    | ~1.70 * 10^38 attempts  | ~2,048 queries / block  |
| Execution Time     | Billions of years       | ~1.04 seconds           |
| Attack Practicality| IMPOSSIBLE              | INSTANTANEOUS & TRIVIAL |
+--------------------+-------------------------+-------------------------+


10. TEST SUITE VERIFICATION MATRIX
-----------------------------------
---------------------------------------------------------------------------
Test Case Name            | Length   | Oracle Queries | Test Result Status
---------------------------------------------------------------------------
1. Single Byte ("X")      | 1 Byte   | ~2,100 queries | PASSED
2. 16-Byte Block Boundary | 16 Bytes | ~4,200 queries | PASSED (Full Pad Added)
3. 32-Byte Exact 2 Blocks | 32 Bytes | ~6,100 queries | PASSED
4. Odd Length (15 Bytes)  | 15 Bytes | ~2,150 queries | PASSED (1-Byte Pad)
5. Multi-Block Sentence   | 80 Bytes | ~9,869 queries | PASSED (3.65 seconds)
---------------------------------------------------------------------------


--------------------------------------------------------------------------------
[PAGE 5: SECURITY IMPLICATIONS, COUNTERMEASURES, & CONCLUSION]
--------------------------------------------------------------------------------

11. SECURITY IMPLICATIONS & ROOT CAUSE ANALYSIS
-----------------------------------------------
1. Confidentiality without Integrity is Broken:
   Encryption alone does not prevent message tampering. Standard AES-CBC mode 
   allows an adversary to alter ciphertext bytes and predictably manipulate 
   the decrypted plaintext.

2. Side-Channel Oracle Leakage:
   Distinguishing between "decryption error" and "padding error" (or leaking 
   this information through execution time) acts as a side-channel oracle that 
   completely bypasses the mathematical strength of the AES cipher.

3. Real-World Exploitations:
   - POODLE Attack (CVE-2014-3566): Forced SSL 3.0 fallback to decrypt session cookies.
   - Lucky Thirteen Attack (CVE-2013-0169): Exploited TLS CBC timing differences.


12. COUNTERMEASURES & MITIGATION STRATEGIES
-------------------------------------------
1. Authenticated Encryption with Associated Data (AEAD) [PRIMARY FIX]:
   Replace CBC mode with AEAD ciphers such as AES-GCM (Galois/Counter Mode) or 
   ChaCha20-Poly1305. AEAD verifies cryptographic authentication tags before 
   decryption, instantly discarding manipulated ciphertexts.

2. Encrypt-then-MAC (EtM):
   If CBC mode must be maintained, compute an HMAC-SHA256 over (IV || Ciphertext). 
   Always verify the HMAC in constant time BEFORE attempting decryption or 
   padding checks.

3. Constant-Time Validation & Generic Error Handling:
   Ensure server responses return uniform generic error messages (e.g., 
   "Decryption Failed") with constant execution time regardless of whether 
   the error was caused by invalid padding or MAC failure.


13. CONCLUSION
--------------
1. The experiment demonstrated that 128-bit AES encryption is rendered completely 
   insecure when paired with unauthenticated CBC mode and a padding oracle.
2. The complete plaintext was recovered byte-by-byte in 2,704 queries (1.044s) 
   without any cryptanalysis of the underlying AES algorithm.
3. Cryptographic systems must combine confidentiality with message authentication 
   (integrity) via AEAD (AES-GCM) or Encrypt-then-MAC to prevent oracle attacks.

================================================================================
RECORD COMPLETED & READY FOR HANDWRITTEN COPY
================================================================================