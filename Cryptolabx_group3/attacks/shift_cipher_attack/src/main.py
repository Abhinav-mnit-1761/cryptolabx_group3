from shift_cipher import encrypt
from brute_force_dictionary import brute_force_dictionary
from chi_square_attack import chi_square_attack

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

