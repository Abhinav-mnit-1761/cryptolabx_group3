def decypher(s,k):
	result = ""
	for char in s:
		if(char.islower()):
			result += chr( (ord(char) - ord('a') + k)%26 + ord('a') )
		else:
			result += chr( (ord(char) - ord('A') + k)%26 + ord('A') ) 
	return result	
	


		
def dec(s,getWord=True):
	print("Input Cypher: " , s)
	if(not(getWord)):	
		for i in range(1,26):
			print(decypher(s,i))
	else:
		with open("../dictionary/english_words.txt" , "r") as file:
			dictionary = set(words.strip().lower() for words in file)
			
		for i in range(1,26):
			message = decypher(s , i)
			if(message.lower() in dictionary):
				print("Decrypted text found in dictionary")
				print("Text: ", message)
		
		
# print(dec("ExxirHergi",False))
