"""
Padding Oracle Attack Implementation
====================================
Recovers plaintext from AES-CBC ciphertext without knowledge of the secret key.
Uses only fundamental bitwise XOR, bytearray manipulation, and oracle feedback.
"""

import time
from typing import Callable, Any

try:
    from aes_cipher import PaddingOracle, pkcs7_unpad
except ImportError:
    from .aes_cipher import PaddingOracle, pkcs7_unpad


def recover_block(
    oracle: PaddingOracle,
    prev_block: bytes,
    target_block: bytes,
    block_size: int = 16,
    verbose: bool = False,
    progress_callback: Callable[[int, int, bytes], Any] | None = None
) -> tuple[bytes, bytes, int]:
    """
    Recovers a single 16-byte plaintext block from target_block using prev_block
    (which is IV for block 1, or C_{i-1} for block i).

    Mathematical Foundation:
        P_i = D_K(C_i) ^ C_{i-1} = I_i ^ C_{i-1}
        When oracle decrypts C_i with modified previous block C'_{i-1}:
        P'_i = D_K(C_i) ^ C'_{i-1} = I_i ^ C'_{i-1}

    Working from right to left (k = 15 down to 0):
        Target padding byte: pad = 16 - k
        For already recovered bytes j > k:
            C'_{i-1}[j] = I_i[j] ^ pad
        For unknown byte k:
            Try candidate guess g in 0..255:
            C'_{i-1}[k] = g
            If oracle returns True:
                I_i[k] = g ^ pad
                P_i[k] = I_i[k] ^ C_{i-1}[k]

    Returns:
        (recovered_plaintext_block, intermediate_state, queries_used)
    """
    intermediate = bytearray(block_size)
    recovered_pt = bytearray(block_size)
    queries_before = oracle.get_query_count()

    # Traverse bytes from right to left
    for k in range(block_size - 1, -1, -1):
        pad = block_size - k
        c_prime = bytearray(block_size)

        # Set already-known trailing bytes to produce the desired pad value
        for j in range(k + 1, block_size):
            c_prime[j] = intermediate[j] ^ pad

        byte_found = False

        # Try all 256 possible byte values
        for g in range(256):
            c_prime[k] = g

            # Query oracle with crafted (IV=c_prime, ciphertext=target_block)
            if oracle.is_padding_valid(bytes(c_prime), target_block):
                # Disambiguate false positive when pad == 1:
                # If original decrypted byte at k-1 happened to form 0x02 0x02,
                # modifying byte k-1 will invalidate it if it was a multi-byte pad.
                if k == block_size - 1:
                    c_prime_check = bytearray(c_prime)
                    c_prime_check[k - 1] ^= 0x01
                    if not oracle.is_padding_valid(bytes(c_prime_check), target_block):
                        continue  # False positive; keep searching

                # Valid guess confirmed
                intermediate[k] = g ^ pad
                recovered_pt[k] = intermediate[k] ^ prev_block[k]
                byte_found = True

                if verbose:
                    char_repr = chr(recovered_pt[k]) if 32 <= recovered_pt[k] <= 126 else f"\\x{recovered_pt[k]:02x}"
                    print(
                        f"  [Byte {k:02d}] Pad: 0x{pad:02x} | Guess: 0x{g:02x} | "
                        f"I[{k:02d}]: 0x{intermediate[k]:02x} | P[{k:02d}]: {char_repr}"
                    )

                if progress_callback:
                    progress_callback(k, pad, bytes(recovered_pt))

                break

        if not byte_found:
            raise RuntimeError(f"Padding oracle attack failed: could not recover byte at index {k}")

    queries_used = oracle.get_query_count() - queries_before
    return bytes(recovered_pt), bytes(intermediate), queries_used


def padding_oracle_attack(
    oracle: PaddingOracle,
    iv: bytes,
    ciphertext: bytes,
    block_size: int = 16,
    verbose: bool = True
) -> dict[str, Any]:
    """
    Executes a complete Padding Oracle Attack against arbitrary AES-CBC ciphertext.
    
    Parameters:
        oracle: The PaddingOracle instance (holds secret key, exposes query endpoint).
        iv: The 16-byte Initialization Vector.
        ciphertext: The AES-CBC ciphertext (must be multiple of block_size).
        block_size: Cipher block size in bytes (default 16 for AES).
        verbose: If True, prints detailed progress information.

    Returns:
        Dictionary containing:
            - 'plaintext': Recovered unpadded bytes
            - 'plaintext_padded': Recovered raw padded bytes
            - 'blocks_recovered': List of recovered block tuples (plaintext, intermediate, queries)
            - 'total_queries': Total number of oracle queries made
            - 'time_elapsed': Total time in seconds
    """
    if len(ciphertext) == 0 or len(ciphertext) % block_size != 0:
        raise ValueError("Ciphertext length must be a non-zero multiple of block_size.")
    if len(iv) != block_size:
        raise ValueError(f"IV length must be exactly {block_size} bytes.")

    start_time = time.time()
    num_blocks = len(ciphertext) // block_size
    ct_blocks = [ciphertext[i * block_size : (i + 1) * block_size] for i in range(num_blocks)]
    prev_blocks = [iv] + ct_blocks[:-1]

    recovered_padded = bytearray()
    blocks_meta = []
    initial_queries = oracle.get_query_count()

    if verbose:
        print("=" * 70)
        print("STARTING PADDING ORACLE ATTACK")
        print(f"Total Blocks: {num_blocks} ({len(ciphertext)} bytes)")
        print(f"Block Size:   {block_size} bytes")
        print("=" * 70)

    for b_idx in range(num_blocks):
        if verbose:
            print(f"\n[*] Attacking Block {b_idx + 1}/{num_blocks}...")

        prev_b = prev_blocks[b_idx]
        curr_b = ct_blocks[b_idx]

        pt_block, inter_block, queries = recover_block(
            oracle=oracle,
            prev_block=prev_b,
            target_block=curr_b,
            block_size=block_size,
            verbose=verbose
        )

        recovered_padded.extend(pt_block)
        blocks_meta.append({
            "block_index": b_idx + 1,
            "plaintext_block": pt_block,
            "intermediate_block": inter_block,
            "queries": queries
        })

        if verbose:
            ascii_preview = "".join(chr(b) if 32 <= b <= 126 else "." for b in pt_block)
            print(f"[+] Block {b_idx + 1} Recovered: {pt_block.hex()} | ASCII: '{ascii_preview}' | Queries: {queries}")

    total_queries = oracle.get_query_count() - initial_queries
    elapsed = time.time() - start_time

    # Strip PKCS#7 padding
    try:
        unpadded_pt = pkcs7_unpad(bytes(recovered_padded), block_size=block_size)
    except ValueError:
        unpadded_pt = bytes(recovered_padded)

    if verbose:
        print("\n" + "=" * 70)
        print("ATTACK COMPLETE")
        print(f"Total Oracle Queries: {total_queries}")
        print(f"Average Per Byte:     {total_queries / len(ciphertext):.2f}")
        print(f"Time Elapsed:         {elapsed:.3f}s")
        print(f"Recovered Plaintext:  {unpadded_pt.decode('utf-8', errors='replace')}")
        print("=" * 70)

    return {
        "plaintext": unpadded_pt,
        "plaintext_padded": bytes(recovered_padded),
        "blocks": blocks_meta,
        "total_queries": total_queries,
        "time_elapsed": elapsed
    }
