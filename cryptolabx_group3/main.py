def display_menu():
	print("\n===== CryptoLabX =====")
	print("1. Encrypt")
	print("2. Decrypt")
	print("3. Attack")
	print("4. Analyze")
	print("5. Exit")
	
while True:
	display_menu()
	
	choice = input("Enter your choice: ")
	
	if choice == "1":
		print("\nEncrypt: Comming Soon")
	elif choice == "2":
		print("\nDecrypt: Comming Soon")
	elif choice == "3":
		print("\nAttack: Comming Soon")
	elif choice == "4":
		print("\nAnalyze: Comming Soon")
	elif choice == "5":
		print("\nThank you for using CryptoLabX.")
		break
	else:
		print("\nInvalid input! Try Again.")
	
