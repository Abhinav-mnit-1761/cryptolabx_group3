from collections import Counter

def analyze_file(filename):
    try:
        with open(filename , "r") as file:
            test = file.read()

            characters = len(text)

            words = len(text.split())

            lines = len(text.splitlines())

            unique_char = 