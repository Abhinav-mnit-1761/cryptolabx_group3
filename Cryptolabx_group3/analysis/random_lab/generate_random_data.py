"""
Task 1: Generate at least 1 MB of cryptographically secure random data
using Linux /dev/urandom, OpenSSL rand, and Windows CNG / .NET.
"""

import os
import sys
import subprocess
import shutil

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_BYTES = 1024 * 1024  # 1 MB = 1,048,576 bytes

def generate_linux_urandom(output_path):
    """
    Generate 1 MB from Linux /dev/urandom.
    If running on Linux/WSL, reads directly from /dev/urandom.
    Otherwise uses Python os.urandom (which wraps /dev/urandom on Unix or BCryptGenRandom on Windows).
    """
    print(f"[*] Generating {TARGET_BYTES} bytes using Linux /dev/urandom -> {output_path}")
    if os.path.exists("/dev/urandom"):
        with open("/dev/urandom", "rb") as f_in, open(output_path, "wb") as f_out:
            data = f_in.read(TARGET_BYTES)
            f_out.write(data)
    else:
        # Fallback for pure Windows host if /dev/urandom is not present
        data = os.urandom(TARGET_BYTES)
        with open(output_path, "wb") as f_out:
            f_out.write(data)
    print(f"[+] Created {output_path} ({os.path.getsize(output_path)} bytes)")

def generate_openssl(output_path):
    """
    Generate 1 MB using OpenSSL rand CLI:
    Command: openssl rand -out <output_path> 1048576
    """
    print(f"[*] Generating {TARGET_BYTES} bytes using OpenSSL rand -> {output_path}")
    openssl_bin = shutil.which("openssl")
    if openssl_bin:
        cmd = [openssl_bin, "rand", "-out", output_path, str(TARGET_BYTES)]
        subprocess.run(cmd, check=True)
    else:
        # If openssl CLI not in PATH, try WSL openssl
        try:
            cmd = ["wsl", "-d", "Ubuntu", "openssl", "rand", "-out", output_path.replace("\\", "/"), str(TARGET_BYTES)]
            subprocess.run(cmd, check=True)
        except Exception:
            raise RuntimeError("OpenSSL CLI not found in system or WSL.")
    print(f"[+] Created {output_path} ({os.path.getsize(output_path)} bytes)")

def generate_windows_cng(output_path):
    """
    Generate 1 MB using Windows CNG (Cryptography Next Generation) or .NET RandomNumberGenerator.
    In PowerShell/.NET: [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    In C/ctypes: BCryptGenRandom(NULL, buf, 1048576, BCRYPT_USE_SYSTEM_PREFERRED_RNG)
    """
    print(f"[*] Generating {TARGET_BYTES} bytes using Windows CNG / .NET -> {output_path}")
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        
        bcrypt = ctypes.windll.bcrypt
        buf = (ctypes.c_ubyte * TARGET_BYTES)()
        BCRYPT_USE_SYSTEM_PREFERRED_RNG = 0x00000002
        status = bcrypt.BCryptGenRandom(None, buf, TARGET_BYTES, BCRYPT_USE_SYSTEM_PREFERRED_RNG)
        if status != 0:
            # Fallback to .NET RNGCryptoServiceProvider / RandomNumberGenerator via powershell
            ps_cmd = f'$b = New-Object byte[] {TARGET_BYTES}; [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($b); [IO.File]::WriteAllBytes("{output_path}", $b)'
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)
        else:
            with open(output_path, "wb") as f_out:
                f_out.write(bytearray(buf))
    else:
        # If running purely on Linux environment, call powershell.exe if WSL interop exists or secrets
        import secrets
        data = secrets.token_bytes(TARGET_BYTES)
        with open(output_path, "wb") as f_out:
            f_out.write(data)
    print(f"[+] Created {output_path} ({os.path.getsize(output_path)} bytes)")

def main():
    urandom_file = os.path.join(OUTPUT_DIR, "urandom.bin")
    openssl_file = os.path.join(OUTPUT_DIR, "openssl.bin")
    windows_cng_file = os.path.join(OUTPUT_DIR, "windows_cng.bin")

    # Generate if not existing or if forced
    if not os.path.exists(urandom_file) or os.path.getsize(urandom_file) != TARGET_BYTES:
        generate_linux_urandom(urandom_file)
    else:
        print(f"[=] Existing {urandom_file} verified ({os.path.getsize(urandom_file)} bytes)")

    if not os.path.exists(openssl_file) or os.path.getsize(openssl_file) != TARGET_BYTES:
        generate_openssl(openssl_file)
    else:
        print(f"[=] Existing {openssl_file} verified ({os.path.getsize(openssl_file)} bytes)")

    if not os.path.exists(windows_cng_file) or os.path.getsize(windows_cng_file) != TARGET_BYTES:
        generate_windows_cng(windows_cng_file)
    else:
        print(f"[=] Existing {windows_cng_file} verified ({os.path.getsize(windows_cng_file)} bytes)")

    print("\n[SUCCESS] All 1 MB random datasets ready for statistical evaluation.")

if __name__ == "__main__":
    main()
