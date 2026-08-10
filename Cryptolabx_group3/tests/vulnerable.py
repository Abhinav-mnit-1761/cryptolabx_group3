import subprocess
import hashlib

password = "admin123"

cmd = input("Enter a command: ")

subprocess.run(cmd, shell=True)

print(hashlib.md5(password.encode()).hexdigest())
