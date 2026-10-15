Laboratory Notebook — Padding Oracle Attack on AES-CBC
Aim
To implement and execute a Padding Oracle Attack against AES-128 in Cipher Block Chaining (CBC) mode with PKCS#7 padding, recover the intermediate decryption state and plaintext byte-by-byte without knowledge of the secret key, and verify the decrypted result.
Brief Theory
The AES block cipher in Cipher Block Chaining (CBC) mode decrypts ciphertext according to the relation P_i = D_K(C_i) ⊕ C_{i-1}, where D_K(C_i) is the intermediate state I_i, and C_0 is the Initialization Vector (IV). PKCS#7 padding ensures plaintext aligns with 16-byte block boundaries by appending N bytes each equal to value N. A padding oracle reveals whether a submitted ciphertext decrypts to valid PKCS#7 padding. Since the attacker controls the preceding ciphertext block C_{i-1}, modifying its bytes directly alters the decrypted plaintext P'_i = I_i ⊕ C'_{i-1}. By systematically altering candidate bytes in C'_{i-1} from right to left (byte 15 down to 0) until the oracle confirms valid padding, the intermediate state byte is deduced as I_i[k] = g ⊕ pad. The original plaintext byte is then recovered as P_i[k] = I_i[k] ⊕ C_{i-1}[k]. Repeating this process across all ciphertext blocks completely recovers the plaintext in linear time (at most 256 queries per byte) without recovering the 128-bit AES key.
Algorithm / Flowchart
Algorithm
1. Intercept the Initialization Vector (IV = C_0) and ciphertext blocks (C_1, C_2, ..., C_M).
2. For each ciphertext block C_i from i = 1 to M, initialize an empty 16-byte intermediate array I_i.
3. Iterate through block byte indices backwards from k = 15 down to 0.
4. Set the expected target padding value pad = 16 - k.
5. Construct probe block C' setting known suffix bytes (j > k) to C'[j] = I_i[j] ⊕ pad.
6. Iterate candidate byte guess g from 0 to 255 for position C'[k] = g.
7. Submit the probe pair (C', C_i) to the padding oracle.
8. If the oracle returns valid padding, verify false positives (for k = 15, mutate C'[14] to confirm 0x01 pad).
9. Calculate intermediate state byte: I_i[k] = g ⊕ pad.
10. Recover the original plaintext byte: P_i[k] = I_i[k] ⊕ C_{i-1}[k].
11. Repeat until all 16 bytes of block P_i are recovered.
12. Concatenate all recovered plaintext blocks into the complete message string.
13. Validate and strip PKCS#7 padding from the recovered plaintext.
Flowchart
Start
  ↓
Receive IV and Ciphertext Blocks
  ↓
Select Target Ciphertext Block C_i
  ↓
Set Byte Index k = 15 (Right to Left)
  ↓
Set Target Pad = 16 - k
  ↓
Set Known Suffix Bytes C'[j] = I_i[j] ⊕ pad
  ↓
Iterate Candidate Guess g in [0, 255] for C'[k]
  ↓
Query Padding Oracle with (C', C_i)
  ↓
Oracle Returns Valid Padding?
  ↓
Verify False-Positive (if k = 15)
  ↓
Calculate Intermediate Byte I_i[k] = g ⊕ pad
  ↓
Recover Plaintext Byte P_i[k] = I_i[k] ⊕ C_{i-1}[k]
  ↓
All Bytes in Block Recovered? (k = 0)
  ↓
All Blocks Processed? (i = M)
  ↓
Strip PKCS#7 Padding
  ↓
Output Recovered Plaintext
  ↓
End

Important Commands
mkdir -p attacks/padding_oracle_attack/{outputs,testcases}

python3 attacks/padding_oracle_attack/src/main.py --demo
python3 attacks/padding_oracle_attack/src/main.py
python3 attacks/padding_oracle_attack/testcases/test_oracle.py

cat attacks/padding_oracle_attack/outputs/result.txt

Observations
- Ciphertext of 1 block (16 bytes) was intercepted with IV: b332d68df081d2e1be12f3fbf99147db and Ciphertext: adaeb0442e3ea6318e843de3edbc6614.
- Padding oracle queries iteratively deduced the intermediate decryption state I_1 byte-by-byte from right to left.
- Intermediate state I_1 recovered: d250bee49ee0a488cd759c9ffd9543df.
- XORing intermediate state with IV yielded the padded plaintext (hex): 616268696e61766973676f6404040404.
- Inferred PKCS#7 padding: 4 padding bytes (0x04 0x04 0x04 0x04).
- Plaintext recovered: "abhinavisgod" (exact match with target plaintext).
- The attack required 2,704 oracle queries (average 169 queries/byte) and completed in 1.044 seconds.
- Test cases across boundary lengths (1 byte, 15 bytes, 16 bytes, 32 bytes, and 80 bytes multi-block) all passed verification successfully.
