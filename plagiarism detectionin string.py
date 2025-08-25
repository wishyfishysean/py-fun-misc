# Importing SequenceMatcher from the difflib module
# This class helps compare sequences (like strings, lists, etc.)
# and tells us how similar they are.
from difflib import SequenceMatcher

# Declaring two string variables that we want to compare
string1 = 'Here we have a sentence, can you believe people try to cheat?'
string2 = 'Here we have a sentence, can you please eat your breakfast?'

# Creating a SequenceMatcher object
# Parameters:
#   - None → we are not providing a custom function to ignore elements
#   - string1 and string2 → the sequences (strings) we want to compare
match = SequenceMatcher(None, string1, string2)

# The .ratio() method returns a float between 0 and 1
#   - 1.0 means the strings are identical
#   - 0.0 means completely different
# We multiply by 100 to express it as a percentage similarity.
result = match.ratio() * 100

# Display the final result
# int(result) converts the float into an integer (e.g., 94.444 → 94)
# so the output looks like "94 %"
print(int(result), "%")
