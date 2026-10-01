"""
Padding Oracle Attack Demonstration Driver
==========================================
Interactive and automated CLI tool to execute padding oracle cryptanalysis.
Saves detailed results to `outputs/result.txt`.
"""

import sys
import os

# Ensure local imports work regardless of execution directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from aes_cipher import PaddingOracle, pkcs7_pad, pkcs7_unpad
from padding_oracle_attack import padding_oracle_attack


def save_result_to_file(
    output_filepath: str,
    original_plaintext: bytes,
    iv: bytes,
    ciphertext: bytes,
    attack_result: dict
) -> None:
    """Writes detailed cryptanalysis results to output file."""
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    
    recovered = attack_result["plaintext"]
    total_queries = attack_result["total_queries"]
    elapsed = attack_result["time_elapsed"]
    blocks = attack_result["blocks"]
    is_valid = (recovered == original_plaintext)

    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write("=" * 75 + "\n")
        f.write("CRYPTOLABX - PADDING ORACLE ATTACK REPORT\n")
        f.write("=" * 75 + "\n\n")

        f.write("--- 1. CIPHERTEXT METADATA ---\n")
        f.write(f"IV (Hex):                  {iv.hex()}\n")
        f.write(f"Ciphertext (Hex):          {ciphertext.hex()}\n")
        f.write(f"Ciphertext Length:         {len(ciphertext)} bytes ({len(ciphertext)//16} blocks)\n\n")

        f.write("--- 2. ATTACK EXECUTION & RECOVERY ---\n")
        f.write(f"Target Plaintext (Original): {original_plaintext.decode('utf-8', errors='replace')}\n")
        f.write(f"Recovered Plaintext:         {recovered.decode('utf-8', errors='replace')}\n")
        f.write(f"Recovered Plaintext (Hex):   {recovered.hex()}\n")
        f.write(f"Verification Successful:     {is_valid}\n\n")

        f.write("--- 3. ORACLE QUERY ANALYSIS ---\n")
        f.write(f"Total Oracle Queries Made:   {total_queries}\n")
        f.write(f"Total Ciphertext Bytes:      {len(ciphertext)}\n")
        f.write(f"Average Queries Per Byte:    {total_queries / len(ciphertext):.2f}\n")
        f.write(f"Execution Time:              {elapsed:.3f} seconds\n\n")

        f.write("--- 4. BLOCK-BY-BLOCK BREAKDOWN ---\n")
        for b in blocks:
            f.write(f"Block #{b['block_index']}:\n")
            f.write(f"  Plaintext (Hex):    {b['plaintext_block'].hex()}\n")
            f.write(f"  Intermediate (Hex): {b['intermediate_block'].hex()}\n")
            f.write(f"  Queries Required:   {b['queries']}\n")
        f.write("\n")

        f.write("--- 5. CRYPTANALYTIC EXPLANATION ---\n")
        f.write("Why modifying the previous ciphertext block affects the target block:\n")
        f.write("In AES-CBC mode, decryption follows the equation:\n")
        f.write("    P_i = D_K(C_i) ^ C_{i-1} = I_i ^ C_{i-1}\n")
        f.write("where D_K is AES decryption under secret key K, and I_i is the intermediate state.\n")
        f.write("When an attacker submits a crafted block C'_{i-1} with target block C_i,\n")
        f.write("the oracle decrypts C_i to I_i and XORs it with C'_{i-1}:\n")
        f.write("    P'_i = I_i ^ C'_{i-1}\n")
        f.write("Because XOR is a bitwise linear operation, the attacker has complete 1-to-1\n")
        f.write("control over P'_i. By observing whether PKCS#7 padding succeeds, the attacker\n")
        f.write("solves for I_i byte-by-byte from right to left without knowing the AES key.\n\n")

        f.write("--- 6. SECURITY RECOMMENDATIONS ---\n")
        f.write("1. Authenticated Encryption: Use AEAD ciphers such as AES-GCM or ChaCha20-Poly1305.\n")
        f.write("2. Encrypt-then-MAC: If CBC must be used, verify HMAC over (IV || Ciphertext) BEFORE decryption.\n")
        f.write("3. Constant-Time Verification: Avoid leaking padding validity differences in error messages or timing.\n")


def run_demo():
    print("\n" + "=" * 70)
    print("DEMO: AES-CBC PADDING ORACLE ATTACK")
    print("=" * 70)

    # 1. Setup Oracle with random secret key (unknown to the attacker)
    oracle = PaddingOracle()
    secret_message = b"Confidential: The AES key is safe, but CBC padding leaks all secrets!"
    
    print(f"\n[*] Original Plaintext:\n    '{secret_message.decode()}'")
    print(f"[*] Length: {len(secret_message)} bytes")

    # 2. Server encrypts message (generates IV and Ciphertext)
    iv, ciphertext = oracle.encrypt_message(secret_message)
    print(f"[*] Server generated AES-128-CBC Ciphertext ({len(ciphertext)} bytes)")
    print(f"    IV  (Hex): {iv.hex()}")
    print(f"    CT  (Hex): {ciphertext.hex()}")
    print("\n[!] The AES key is NOT accessible to the attacker.")
    print("[!] Attacker will only submit crafted (IV, Ciphertext) blocks to the Oracle.")

    # 3. Launch the Padding Oracle Attack
    oracle.reset_query_count()
    result = padding_oracle_attack(
        oracle=oracle,
        iv=iv,
        ciphertext=ciphertext,
        block_size=16,
        verbose=True
    )

    # 4. Save results to outputs/result.txt
    output_path = os.path.join(CURRENT_DIR, "..", "outputs", "result.txt")
    save_result_to_file(output_path, secret_message, iv, ciphertext, result)
    print(f"\n[+] Detailed analysis report saved to: {os.path.abspath(output_path)}")


def run_custom():
    user_input = input("\nEnter custom message to encrypt and recover: ").strip()
    if not user_input:
        print("[!] Empty message. Using default.")
        user_input = "Lab Test Message for Padding Oracle"
    
    msg_bytes = user_input.encode("utf-8")
    oracle = PaddingOracle()
    iv, ciphertext = oracle.encrypt_message(msg_bytes)
    oracle.reset_query_count()

    print(f"\n[*] Encrypted with unknown secret AES key.")
    print(f"    IV: {iv.hex()}")
    print(f"    CT: {ciphertext.hex()} ({len(ciphertext)} bytes)")

    result = padding_oracle_attack(
        oracle=oracle,
        iv=iv,
        ciphertext=ciphertext,
        block_size=16,
        verbose=True
    )

    output_path = os.path.join(CURRENT_DIR, "..", "outputs", "result.txt")
    save_result_to_file(output_path, msg_bytes, iv, ciphertext, result)
    print(f"\n[+] Result saved to: {os.path.abspath(output_path)}")


def run_test_suite():
    print("\n" + "=" * 70)
    print("RUNNING COMPREHENSIVE PADDING ORACLE TEST SUITE")
    print("=" * 70)

    test_cases = [
        ("Single Byte", b"X"),
        ("Exact 16 Bytes (Boundary Test)", b"1234567890123456"),
        ("Exact 32 Bytes (2 Full Blocks)", b"1234567890123456abcdefghijklmnop"),
        ("Odd Length (15 Bytes)", b"Testing15Bytes!"),
        ("Multi-Block Sentence", b"Padding Oracle attacks break unauthenticated CBC ciphers completely."),
    ]

    oracle = PaddingOracle()
    all_passed = True

    for name, msg in test_cases:
        print(f"\n--- Testing: {name} (Length: {len(msg)} bytes) ---")
        iv, ct = oracle.encrypt_message(msg)
        oracle.reset_query_count()

        res = padding_oracle_attack(oracle, iv, ct, block_size=16, verbose=False)
        recovered = res["plaintext"]
        queries = res["total_queries"]
        passed = (recovered == msg)

        print(f"  Original:   '{msg.decode()}'")
        print(f"  Recovered:  '{recovered.decode()}'")
        print(f"  Queries:    {queries} (Avg: {queries / len(ct):.1f} per byte)")
        print(f"  Status:     {'[PASSED]' if passed else '[FAILED]'}")

        if not passed:
            all_passed = False

    print("\n" + "=" * 70)
    print(f"TEST SUITE RESULT: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print("=" * 70)


def print_explanation_summary():
    print("\n" + "=" * 70)
    print("PADDING ORACLE ATTACK SUMMARY")
    print("=" * 70)
    print("""
Key Concept:
1. AES-CBC Decryption: P_i = D_K(C_i) ^ C_{i-1} = I_i ^ C_{i-1}
   - D_K(C_i) is the intermediate state I_i before the XOR step.
   - C_{i-1} is the previous ciphertext block (or IV for block 1).

2. How the Oracle Leaks Information:
   - A padding oracle receives (C'_{i-1}, C_i) and only tells us if PKCS#7
     padding is VALID or INVALID.
   - By crafting C'_{i-1}, the attacker modifies the decrypted plaintext P'_i
     directly: P'_i = I_i ^ C'_{i-1}.

3. Right-to-Left Recovery:
   - To find the last byte I_i[15], test candidate bytes g in 0..255 for C'_{i-1}[15]
     until the oracle returns True (valid pad 0x01).
   - Once found, I_i[15] = g ^ 0x01.
   - Actual plaintext byte is P_i[15] = I_i[15] ^ C_{i-1}[15].
   - Repeat for all bytes from index 15 down to 0 using pad = 16 - k.

4. Query Complexity:
   - Brute-force key search: 2^128 operations (impossible).
   - Padding Oracle: At most 256 queries per byte (~128 on average).
   - For a 16-byte block: ~2,048 queries (executed in fractions of a second).

5. Prevention:
   - Authenticated Encryption with Associated Data (AEAD): AES-GCM.
   - Encrypt-then-MAC: Verify HMAC over ciphertext BEFORE decrypting.
    """)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo()
        return

    while True:
        print("\n" + "=" * 50)
        print("   CryptoLabX - Padding Oracle Attack")
        print("=" * 50)
        print("1. Run Default Demonstration Attack")
        print("2. Encrypt & Recover Custom Message")
        print("3. Run Comprehensive Test Suite")
        print("4. View Attack Theory & Analysis Summary")
        print("0. Exit")
        print("=" * 50)

        choice = input("Enter choice (0-4): ").strip()

        if choice == "1":
            run_demo()
        elif choice == "2":
            run_custom()
        elif choice == "3":
            run_test_suite()
        elif choice == "4":
            print_explanation_summary()
        elif choice == "0":
            print("Exiting Padding Oracle Attack module.")
            break
        else:
            print("Invalid selection. Please choose 0-4.")


if __name__ == "__main__":
    main()
