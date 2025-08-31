from googlesearch import search
import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

text = "This is a sample sentence to check online."
similarity_scores = []

for url in search(text, num=3, stop=3):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        webpage_text = soup.get_text()
        score = SequenceMatcher(None, text, webpage_text).ratio()
        similarity_scores.append(score)
    except:
        continue

if similarity_scores:
    print(f"Max similarity found: {max(similarity_scores)*100:.2f}%")
else:
    print("No matches found online.")
