from analysis.file_analysis import analyze_file
from utils.logger import write_log

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
        print("Attack - Coming Soon")

    elif choice == "4":
        write_log("Analyze")
        analyze_file()

    elif choice == "5":
        write_log("Exit")
        print("Thank you for using CryptoLabX!")
        break

    else:
        print("Invalid choice. Please try again.")

