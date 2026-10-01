from analysis.file_analysis import analyze_file
from utils.logger import write_log
import subprocess
import sys

def show_menu():
    print("\n===== CryptoLabX =====")
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Attack")
    print("4. Analyze")
    print("5. Exit")


while True:
    show_menu()

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        write_log("Encrypt")
        print("Encrypt - Coming Soon")

    elif choice == "2":
        write_log("Decrypt")
        print("Decrypt - Coming Soon")

    elif choice == "3":
        write_log("Attack")
        print("\n--- Attack Modules ---")
        print("1. Shift Cipher Attack")
        print("2. Vigenere Cipher Attack")
        print("3. Padding Oracle Attack (AES-CBC)")
        print("4. Back to Main Menu")
        att_choice = input("Select attack (1-4): ").strip()
        if att_choice == "1":
            subprocess.run([sys.executable, "attacks/shift_cipher_attack/src/main.py"])
        elif att_choice == "2":
            subprocess.run([sys.executable, "attacks/vigenere_attack/main.py"])
        elif att_choice == "3":
            subprocess.run([sys.executable, "attacks/padding_oracle_attack/src/main.py"])
        elif att_choice == "4":
            pass
        else:
            print("Invalid attack choice.")

    elif choice == "4":
        write_log("Analyze")
        analyze_file()

    elif choice == "5":
        write_log("Exit")
        print("Thank you for using CryptoLabX!")
        break

    else:
        print("Invalid choice. Please try again.")
