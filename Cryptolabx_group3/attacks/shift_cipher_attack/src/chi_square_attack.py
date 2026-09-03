def getScore(s,k):
	freq = [0.08167, 0.01492, 0.02782, 0.04253, 	
		0.12702,0.02228,0.02015,0.06094,0.06966,0.00153,	
		0.00772,0.04025,0.02406,0.06749,0.07507,0.01929,
		0.00095,0.05987,0.06327,0.09056,0.02758,0.00978,
		0.02360,0.00150,0.01974, 0.00074]
		
	
	
import string
def decypher(s,k): 
	result = "" 
	for char in s: 
		if(char.islower()): 
			result += chr( (ord(char) - ord('a') + k)%26 + ord('a') ) 
		else: 
			result += chr( (ord(char) - ord('A') + k)%26 + ord('A') ) 
	return result

ENGLISH_FREQ = {
    'A': 0.0812, 'B': 0.0149, 'C': 0.0271, 'D': 0.0432,
    'E': 0.1202, 'F': 0.0230, 'G': 0.0203, 'H': 0.0592,
    'I': 0.0731, 'J': 0.0010, 'K': 0.0069, 'L': 0.0398,
    'M': 0.0261, 'N': 0.0695, 'O': 0.0768, 'P': 0.0182,
    'Q': 0.0011, 'R': 0.0602, 'S': 0.0628, 'T': 0.0910,
    'U': 0.0288, 'V': 0.0111, 'W': 0.0209, 'X': 0.0017,
    'Y': 0.0211, 'Z': 0.0007
}


def chi_square_score(text):
    text = text.upper()

    letters = [c for c in text if c in string.ascii_uppercase]
    total = len(letters)

    if total == 0:
        return float('inf')

    score = 0

    for letter in string.ascii_uppercase:
        observed = letters.count(letter)
        expected = ENGLISH_FREQ[letter] * total

        score += (observed - expected) ** 2 / expected

    return score
    
def chi_square_attack(ciphertext):
    best_key = 0
    best_score = float("inf")
    w = ""

    for key in range(26):
        decrypted = decypher(ciphertext, key)
        score = chi_square_score(decrypted)

        if (score < best_score):
            best_score = score
            best_key = key
            w = decrypted

    return best_key, best_score,w

