def shift(c,k):
	if(c.isalpha()):
		if(c.islower()):
			return chr( (ord(c)-ord('a') + k) % 26 + ord('a'))
		else:
			return chr((ord(c)-ord('A') + k) % 26 + ord('A'))
	else:
		print("Wrong input")
		return "-1"
		

def encrypt(s,k):
	result = ""
		
	for i in range(len(s)):
		char = s[i]
		result += shift(char,k)
	
	return result
	
print(encrypt("Atten1Dance" , 4))
		
		
		



