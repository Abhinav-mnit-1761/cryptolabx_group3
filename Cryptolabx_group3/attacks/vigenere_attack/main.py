from vigenere import *


# Read ciphertext
with open("../../datasets/plaintext_veg.txt", "r") as f:
    raw_ciphertext = f.read()


# 1. Preprocess
ciphertext = clean_ciphertext(raw_ciphertext)

print("=" * 60)
print("VIGENERE CIPHER CRYPTANALYSIS")
print("=" * 60)

print("\nCiphertext length:", len(ciphertext))


# 2. Kasiski examination
patterns, distances, candidates = kasiski_analysis(ciphertext)

print("\n--- KASISKI ANALYSIS ---")

print("\nRepeated patterns:")
for pattern, positions in patterns.items():
    print(pattern, positions)

print("\nDistances:")
for pattern, distance in distances:
    print(f"{pattern}: {distance}")

print("\nCandidate key lengths:")
print(candidates[:10])


# 3. Use candidate key lengths
candidate_lengths = [length for length, count in candidates[:10]]

if not candidate_lengths:
    candidate_lengths = list(range(2, 11))


# 4. Calculate IC for candidates
print("\n--- INDEX OF COINCIDENCE ---")

ic_results = {}

for key_length in candidate_lengths:
    groups = split_into_groups(ciphertext, key_length)

    ic_values = [calculate_ic(group) for group in groups]
    average_ic = sum(ic_values) / len(ic_values)

    ic_results[key_length] = average_ic

    print(
        f"Key length {key_length}: "
        f"Average IC = {average_ic:.4f}"
    )


# 5. Choose key length
estimated_key_length = max(
    ic_results,
    key=ic_results.get
)

print("\nEstimated key length:", estimated_key_length)


# 6. Split into groups
groups = split_into_groups(
    ciphertext,
    estimated_key_length
)


# 7. Frequency analysis
print("\n--- FREQUENCY ANALYSIS ---")

for i, group in enumerate(groups):
    frequencies = frequency_analysis(group)

    print(f"\nGroup {i + 1}:")
    print(group)
    print(
        " ".join(
            f"{letter}:{freq:.3f}"
            for letter, freq in frequencies.items()
            if freq > 0
        )
    )


# 8. Recover key
key = find_key(groups)

print("\nRecovered key:", key)


# 9. Decrypt
plaintext = vigenere_decrypt(ciphertext, key)

print("\n--- RECOVERED PLAINTEXT ---")
print(plaintext)


# 10. Verification
result = verify(ciphertext, plaintext, key)

print("\n--- VERIFICATION ---")
print("Re-encryption successful:", result)


# 11. Save output
with open("outputs/result.txt", "w") as f:
    f.write(f"Estimated key length: {estimated_key_length}\n")
    f.write(f"Recovered key: {key}\n\n")
    f.write("Recovered plaintext:\n")
    f.write(plaintext)
    f.write("\n\nVerification: ")
    f.write(str(result))

print("\nResult saved to outputs/result.txt")
