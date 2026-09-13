from shift_cipher import encrypt
from brute_force_dictionary import brute_force_dictionary
from chi_square_attack import chi_square_attack

while(True):
	t = int(input("Enter 1 for message or 2 for ciphertext or 0 for exit: "))
	if(t == 1):

		text = input("Enter message: ")
		while(True):
			key = int(input("Enter key(0 to 25): "))
			if(key < 0 or key > 25):
				print("Enter valid input\n")
			else:
				break


		cipher = encrypt(text , key)
		b_key,m,word1 = brute_force_dictionary(cipher)
		c_key , score , word2 = chi_square_attack(cipher)
		print(b_key," : ", word1 )
		print(c_key , " : " , score, " : " , word2)
	elif(t == 2):
		cipher = input("Enter ciphertext: ")
		
		print("Performing chi_Square_attack...")
		c_key , score , word = chi_square_attack(cipher,True)
		print("-----------------")
		print("Best values: ")
		print("Key: ", c_key)
		print("Word: ",word)
		
	elif(t == 0):
		break
	else:
		print("Enter valid input!!!")
		

