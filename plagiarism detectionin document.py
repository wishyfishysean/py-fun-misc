# Importing SequenceMatcher from the difflib module
# SequenceMatcher helps compare two sequences (strings, lists, etc.)
# and gives a similarity ratio between 0 and 1.
from difflib import SequenceMatcher

# Opening two text files at the same time using 'with'
# - 'with' ensures the files are automatically closed after use
# - we open doc1.txt as first_file, and doc2.txt as second_file
with open('doc1.txt', 'r') as first_file, open('doc2.txt', 'r') as second_file:

    # Reading the full content of both text files into strings
    file1 = first_file.read()
    file2 = second_file.read()

    # Creating a SequenceMatcher object and getting similarity ratio
    # Parameters:
    #   None → no custom ignore function
    #   file1, file2 → the two strings (documents) we want to compare
    # .ratio() returns a float between 0.0 and 1.0
    ab = SequenceMatcher(None, file1, file2).ratio()

    # Multiply by 100 to convert the ratio into a percentage
    # Convert float to int so result looks clean (e.g., 87.52 → 87)
    result = int(ab * 100)

    # Display the similarity result as "xx% Plagiarized Content"
    print(f"{result}% Plagiarized Content")
