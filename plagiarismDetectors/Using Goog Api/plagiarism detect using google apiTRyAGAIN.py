import tkinter as tk
from tkinter import filedialog
from difflib import SequenceMatcher
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import nltk

# --- Make sure you have nltk punkt tokenizer ---
# pip install nltk
# nltk.download('punkt')
from nltk.tokenize import sent_tokenize

file_path = ""

# --- Functions ---
def select_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    label_file.config(text=file_path)

def check_online_plagiarism():
    if not file_path:
        result_label.config(text="⚠️ Please select a file")
        return

    with open(file_path, "r") as f:
        text = f.read()

    sentences = sent_tokenize(text)
    max_scores = []

    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 20:
            continue  # skip very short sentences

        scores = []
        try:
            for url in search(sentence, num=2, stop=2, pause=2):
                try:
                    r = requests.get(url, timeout=3)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    webpage_text = soup.get_text()
                    score = SequenceMatcher(None, sentence, webpage_text).ratio()
                    scores.append(score)
                except:
                    continue
            if scores:
                max_scores.append(max(scores))
        except:
            continue

    if max_scores:
        overall_similarity = sum(max_scores)/len(max_scores) * 100
        result_label.config(text=f"Estimated Online Similarity: {overall_similarity:.2f}%")
    else:
        result_label.config(text="No matches found online.")

# --- GUI ---
root = tk.Tk()
root.title("Online Plagiarism Detector")

tk.Button(root, text="Select File", command=select_file).pack(pady=5)
label_file = tk.Label(root, text="No file selected")
label_file.pack()

tk.Button(root, text="Check Online Plagiarism", command=check_online_plagiarism).pack(pady=10)
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
