
	
from collections import Counter

eng_freq = [
	0.0812, 0.0149, 0.0271, 0.0432, 0.1202, 0.0230,
	0.0209, 0.0592, 0.0768, 0.0015, 0.0077, 0.0402,
	0.0240, 0.0674, 0.0750, 0.0192, 0.0009, 0.0602,
	0.0628, 0.0910, 0.0288, 0.0111, 0.0209, 0.0017,
	0.0211, 0.0007
]

def clean_ciphertext(ciphertext):
	return ''.join(c.upper() for c in ciphertext if c.isalpha())

def find_repeated_patterns(ciphertext,min_len=3,max_len=5):
	patterns = {}
	
	for length in range(min_len,max_len+1):
		seen = {}
		
		for i in range(len(ciphertext) - length+1):
			pattern = ciphertext[i:i+length]
			seen.setdefault(pattern,[]).append(i)
		
		for pattern,position in seen.items():
			if(len(position) > 1):
				patterns[pattern] = position
	return patterns
	
def calculate_distances(patterns):
	distances = []
	
	for pattern, positions in patterns.items():
		for i in range(len(positions)):
			for j in range(i+1, len(positions)):
				distances.append(
					(pattern, positions[j] - positions[i])
				)
	return distances

def find_factors(n):
	factors = []
	
	for i in range(2 , n+1 ):
		if(n%i == 0):
			factors.append(i)
	return factors
	
def kasiski_analysis(ciphertext):
	patterns = find_repeated_patterns(ciphertext)
	distances = calculate_distances(patterns)
	
	factor_count = Counter()
	
	for pattern, distance in distances:
		for factor in find_factors(distance):
			if factor<=20:
				factor_count[factor] += 1
	
	candidates = factor_count.most_common()
	
	return patterns, distances, candidates
	

def calculate_ic(text):
	n = len(text)
	
	if n<=1:
		return 0
		
	counts = Counter(text)
	
	num = sum(freq*(freq-1) for freq in counts.values())
	den = n * (n-1)
	
	return num / den
	
def split_into_groups(ciphertext, key_length):
	return [
		ciphertext[i::key_length] for i in range(key_length)
	]

def frequency_analysis(group):
	counts = Counter(group)
	total = len(group)
	
	frequencies = {}
	
	for i in range(26):
		letter = chr(ord('A') + i)
		frequencies[letter] = counts.get(letter,0)/total
	return frequencies

def find_shift(group):
	n = len(group)
	counts = Counter(group)
	
	best_shift = 0
	best_score = float('inf')
	
	for shift in range(26):
		score = 0
		
		for i in range(26):
			plaintext_index = (i - shift) % 26
			
			expected = eng_freq[plaintext_index]*n
			observed = counts.get(chr(ord('A') + i),0)
			if expected > 0:
				score += (observed - expected)**2 / expected
		if score < best_score:
			best_score = score
			best_shift = shift
	return best_shift

def find_key(groups):
	key = ""
	
	for group in groups:
		shift = find_shift(group)
		key += chr(ord('A') + shift)
	return key
	
def vigenere_decrypt(ciphertext,key):
	plaintext = []
	
	for i,c in enumerate(ciphertext):
		p_value = ord(c) - ord('A')
		k_value = ord(key[i%len(key)]) - ord('A')
		
		p_value = (p_value - k_value) % 26
		
		plaintext.append(chr(p_value + ord('A')))
		
	return ''.join(ciphertext)

def vigenere_encrypt(plaintext, key):
    ciphertext = []

    for i, p in enumerate(plaintext):
        p_value = ord(p) - ord('A')
        k_value = ord(key[i % len(key)]) - ord('A')

        c_value = (p_value + k_value) % 26

        ciphertext.append(chr(c_value + ord('A')))

    return ''.join(ciphertext)
    	
def verify(original_ciphertext, plaintext, key):
	encrypted = vigenere_encrypt(plaintext , key)
	return encrypted == original_ciphertext
		
