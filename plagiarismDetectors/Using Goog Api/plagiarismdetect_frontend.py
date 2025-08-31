import tkinter as tk
from tkinter import filedialog
from difflib import SequenceMatcher

# --- Global variables to hold file paths ---
file1_path = ""
file2_path = ""

# --- Functions ---
def select_file1():
    global file1_path
    file1_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    label_file1.config(text=file1_path)

def select_file2():
    global file2_path
    file2_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    label_file2.config(text=file2_path)

def check_plagiarism():
    if not file1_path or not file2_path:
        result_label.config(text="⚠️ Please select both files")
        return

    with open(file1_path, "r") as f1, open(file2_path, "r") as f2:
        text1 = f1.read()
        text2 = f2.read()

    similarity = SequenceMatcher(None, text1, text2).ratio()
    result_label.config(text=f"Plagiarism: {similarity*100:.2f}%")

# --- GUI ---
root = tk.Tk()
root.title("Plagiarism Detector")

tk.Button(root, text="Select First File", command=select_file1).pack(pady=5)
label_file1 = tk.Label(root, text="No file selected")
label_file1.pack()

tk.Button(root, text="Select Second File", command=select_file2).pack(pady=5)
label_file2 = tk.Label(root, text="No file selected")
label_file2.pack()

tk.Button(root, text="Check Plagiarism", command=check_plagiarism).pack(pady=10)
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
