# ==============================================================================
# CRYPTOGRAPHIC PRIME GENERATION USING MILLER-RABIN PRIMALITY TEST
# ==============================================================================
# Script: main.py
# Description: Generates a 512-bit probable prime, executes multi-round
#              Miller-Rabin testing, logs detailed experimental metrics,
#              verifies correctness using multiple independent methods, and
#              exports results to outputs/result.txt.
# ==============================================================================

import os
import sys
import time

from miller_rabin import (
    generate_prime,
    verify_prime,
    decompose,
    miller_rabin_round
)


def format_table(params):
    """Format experimental results as a clean text table."""
    col1_width = 32
    col2_width = 80
    border = "+" + "-" * (col1_width + 2) + "+" + "-" * (col2_width + 2) + "+"
    header = f"| {'Parameter':<{col1_width}} | {'Value':<{col2_width}} |"

    lines = [
        border,
        header,
        border
    ]

    for param, val in params:
        val_str = str(val)
        if len(val_str) > col2_width:
            # Wrap long strings across multiple lines
            first = True
            while val_str:
                chunk = val_str[:col2_width]
                val_str = val_str[col2_width:]
                p_text = param if first else ""
                lines.append(f"| {p_text:<{col1_width}} | {chunk:<{col2_width}} |")
                first = False
        else:
            lines.append(f"| {param:<{col1_width}} | {val_str:<{col2_width}} |")

    lines.append(border)
    return "\n".join(lines)


def run_experiment(bit_length=512, rounds=40):
    print("=" * 80)
    print("TASK: CRYPTOGRAPHIC PRIME GENERATION USING MILLER-RABIN")
    print(f"Objective: Generate a probable prime of {bit_length}-bit length using Miller-Rabin.")
    print("=" * 80)
    print("\n[Step 1] Generating prime candidate...")
    print(f" -> Assigned bit length: {bit_length}")
    print(f" -> Number of Miller-Rabin test rounds: {rounds}")
    print(" -> Pre-filter: Small prime trial division (primes <= 1000)")
    
    t0 = time.perf_counter()
    prime, stats = generate_prime(bit_length=bit_length, rounds=rounds, use_prefilter=True)
    t1 = time.perf_counter()

    print("\n[Step 2] Candidate Found!")
    print(f" -> Generated in {stats['execution_time']:.4f} seconds.")
    print(f" -> Total odd candidates generated: {stats['candidates_tested']}")
    print(f" -> Rejected by small-prime pre-filter: {stats['prefilter_rejected']}")
    print(f" -> Tested with Miller-Rabin: {stats['mr_candidates_tested']}")

    # Formatted experimental results table as requested by the assignment
    table_data = [
        ("Assigned bit length", stats['assigned_bit_length']),
        ("Generated prime candidate (Decimal)", stats['candidate']),
        ("Generated prime candidate (Hex)", stats['hex']),
        ("Actual bit length of the candidate", stats['actual_bit_length']),
        ("Number of candidates tested", stats['candidates_tested']),
        ("Number of Miller–Rabin rounds", stats['mr_rounds']),
        ("Total execution time", f"{stats['execution_time']:.4f} seconds"),
    ]

    table_output = format_table(table_data)

    print("\n" + "=" * 80)
    print("1. EXPERIMENTAL RESULTS TABLE")
    print("=" * 80)
    print(table_output)

    # Step 3: Verification
    print("\n" + "=" * 80)
    print("3. VERIFICATION")
    print("=" * 80)

    # 3.1 Bit length demonstration
    print("\n[Verification 1] Bit Length Check:")
    print(f" - Candidate value: {prime}")
    print(f" - Bit length computed: {prime.bit_length()}")
    print(f" - Bit 511 (MSB): {(prime >> 511) & 1} (Must be 1 for exact 512-bit range)")
    print(f" - Bit 0 (LSB): {prime & 1} (Must be 1 for odd number)")
    print(f" - Exact 512-bit range valid: {2**511 <= prime < 2**512}")
    assert prime.bit_length() == bit_length, "Bit length mismatch!"

    # 3.2 Miller-Rabin with specified bases
    specified_bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    print(f"\n[Verification 2] Miller-Rabin Test with Specified Bases:")
    s, d = decompose(prime)
    print(f" - Decomposition of (n - 1) = 2^s * d:")
    print(f"   s = {s}")
    print(f"   d bit length = {d.bit_length()} bits")
    print(" - Evaluation across deterministic bases:")
    
    mr_logs = []
    for base in specified_bases:
        passed, msg = miller_rabin_round(prime, base, s, d)
        status_symbol = "[PASS]" if passed else "[FAIL]"
        log_line = f"   {status_symbol} {msg}"
        print(log_line)
        mr_logs.append(log_line)
        assert passed, f"Failed at base {base}!"

    # 3.3 Independent Primality Checks
    print(f"\n[Verification 3] Independent Primality-Checking Methods:")
    
    # 3.3.1 Small prime trial division
    print(" (a) Small Prime Trial Division (All primes <= 2000):")
    v_report = verify_prime(prime, assigned_bit_length=bit_length, specified_bases=specified_bases)
    print(f"     -> Trial division passed: {v_report['trial_division_passed']} (No factors <= 2000)")
    assert v_report['trial_division_passed'], "Failed small prime trial division!"

    # 3.3.2 Fermat Primality Test
    print(" (b) Fermat's Little Theorem Test (Independent bases [41, 43, 47, 53, 59, 61, 67, 71, 73, 79]):")
    fermat_passed = v_report['fermat_test_passed']
    print(f"     -> Fermat test passed for all independent bases: {fermat_passed}")
    for base, ok, _ in v_report['fermat_details'][:5]:
        print(f"        Base {base}^(n-1) mod n == 1: {ok}")
    print("        ... (remaining independent bases verified: True)")
    assert fermat_passed, "Failed Fermat primality check!"

    # 3.3.3 Baillie-PSW Strong Lucas Test
    print(" (c) Strong Lucas Probable Prime Test (Baillie-PSW):")
    lucas_passed = v_report['strong_lucas_passed']
    print(f"     -> Strong Lucas test passed: {lucas_passed}")
    assert lucas_passed, "Failed Strong Lucas primality check!"

    print(f"\n[Overall Verification Result]: {'SUCCESS - Cryptographically Strong Probable Prime' if v_report['overall_verified'] else 'FAILED'}")

    # Step 4: Save outputs to outputs/result.txt
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "result.txt")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("CRYPTOGRAPHIC PRIME GENERATION USING MILLER-RABIN PRIMALITY TEST\n")
        f.write("=" * 80 + "\n\n")
        f.write("1. EXPERIMENTAL RESULTS\n")
        f.write(table_output + "\n\n")
        f.write("2. CANDIDATE DETAILS\n")
        f.write(f"Decimal Representation:\n{prime}\n\n")
        f.write(f"Hexadecimal Representation:\n{stats['hex']}\n\n")
        f.write("3. VERIFICATION REPORT\n")
        f.write(f"- Assigned bit length: {bit_length}\n")
        f.write(f"- Actual bit length: {prime.bit_length()} (VALID: {v_report['bit_length_valid']})\n")
        f.write(f"- Decomposition (n - 1) = 2^{s} * d\n")
        f.write(f"- Miller-Rabin with Specified Bases {specified_bases}:\n")
        for line in mr_logs:
            f.write(f"  {line}\n")
        f.write(f"\n- Independent Small Prime Trial Division (primes <= 2000): PASSED\n")
        f.write(f"- Independent Fermat's Little Theorem Test (10 bases): PASSED\n")
        f.write(f"- Independent Strong Lucas Probable Prime Test (Baillie-PSW): PASSED\n")
        f.write(f"\nOVERALL VERIFICATION STATUS: VERIFIED PROBABLE PRIME\n")

    print(f"\n[File Saved] Results successfully written to: {output_path}")
    return prime, stats, v_report


if __name__ == "__main__":
    run_experiment(bit_length=512, rounds=40)
