def decypher(s,k):
	result = ""
	for char in s:
		if(char.islower()):
			result += chr( (ord(char) - ord('a') + k)%26 + ord('a') )
		else:
			result += chr( (ord(char) - ord('A') + k)%26 + ord('A') ) 
	return result	
	


		
def brute_force_dictionary(s,getWord=True):
	
	print("Input Cypher: " , s)
	if(not(getWord)):	
		for i in range(1,26):
			print(decypher(s,i))
	else:
		key = -1
		with open("../dictionary/english_words.txt" , "r") as file:
			dictionary = set(word.strip().lower() for word in file)
		#print(type(dictionary))
		maxcount = -1
		w = ""
		for i in range(0,26):
			count = 0
			message = decypher(s, i)

			words = message.lower().split()

			for word in words:
				if word in dictionary:
					count = count + 1
					w = word
			if(count > maxcount):
				maxcount = count
				key = i
				wrd = w
		return key, maxcount, decypher(s, key)
		
		
#print(brute_force_dictionary("ExxirHergi"))
