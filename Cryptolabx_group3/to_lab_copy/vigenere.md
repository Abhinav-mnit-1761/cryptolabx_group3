Laboratory Notebook — Cryptanalysis of Vigenère Cipher
Aim
To implement the cryptanalysis of a Vigenère cipher using Kasiski Examination and Frequency Analysis, recover the probable key, decrypt the ciphertext, and verify the result by re-encryption.
Brief Theory
The Vigenère cipher is a polyalphabetic substitution cipher that uses a repeating keyword to encrypt plaintext. Each key character determines a different Caesar shift. In cryptanalysis, the Kasiski Examination helps estimate the key length by finding repeated sequences in the ciphertext and analyzing the distances between their occurrences. Factors common to these distances are possible key lengths. The Index of Coincidence (IC) is then used to support the selection of the key length by checking whether groups of characters have frequency distributions similar to English. Once the key length is estimated, the ciphertext is divided into groups, and frequency analysis is applied to each group to determine its Caesar shift. These shifts are combined to recover the Vigenère key. Finally, the ciphertext is decrypted and re-encrypted with the recovered key to verify correctness.
Algorithm / Flowchart
Algorithm
1. Read the Vigenère ciphertext.
2. Remove spaces and special characters and convert it to uppercase.
3. Find repeated character patterns in the ciphertext.
4. Calculate the distances between repeated occurrences.
5. Find factors of these distances and obtain candidate key lengths.
6. Calculate the Index of Coincidence for candidate key lengths.
7. Select the most probable key length.
8. Divide the ciphertext into groups according to the key length.
9. Perform frequency analysis on each group.
10. Determine the Caesar shift for each group.
11. Combine the shifts to obtain the probable Vigenère key.
12. Decrypt the ciphertext using the recovered key.
13. Re-encrypt the recovered plaintext and compare it with the original ciphertext.
Flowchart
Start
  ↓
Read Ciphertext
  ↓
Clean & Normalize Ciphertext
  ↓
Find Repeated Patterns
  ↓
Calculate Distances
  ↓
Find Factors
  ↓
Kasiski Analysis
  ↓
Candidate Key Lengths
  ↓
Calculate Index of Coincidence
  ↓
Estimate Key Length
  ↓
Split Ciphertext into Groups
  ↓
Frequency Analysis
  ↓
Find Caesar Shift for Each Group
  ↓
Recover Vigenère Key
  ↓
Decrypt Ciphertext
  ↓
Re-encrypt Plaintext
  ↓
Compare with Original Ciphertext
  ↓
Verification
  ↓
End

Important Commands
mkdir -p attacks/vigenere_attack/{outputs,testcases}

touch attacks/vigenere_attack/main.py
touch attacks/vigenere_attack/vigenere.py

python3 main.py

Observations
- The ciphertext was successfully cleaned and normalized.
- Kasiski Examination identified repeated ciphertext patterns and their distances.
- The most significant candidate key lengths included 7 and 14.
- Index of Coincidence strongly supported 14 as the probable key length, with an average IC of approximately 0.0644.
- Frequency analysis of the 14 groups produced the recovered key: