def analyze_file():
    filename = input("Enter file name (e.g. sample1.txt): ")
    filename = "datasets/" + filename

    try:
        with open(filename, "r") as file:
            text = file.read()

        characters = len(text)
        words = len(text.split())
        lines = len(text.splitlines())
        unique_characters = len(set(text))

        letter_frequency = {}

        for char in text.lower():
            if char.isalpha():
                letter_frequency[char] = letter_frequency.get(char, 0) + 1

        print("\n===== File Analysis =====")
        print("Characters :", characters)
        print("Words :", words)
        print("Lines :", lines)
        print("Unique Characters :", unique_characters)

        print("\nLetter Frequency")
        for letter in sorted(letter_frequency):
            print(f"{letter} : {letter_frequency[letter]}")

    except FileNotFoundError:
        print("File not found!")