import tkinter as tk
from tkinter import filedialog, messagebox

# --- Main Application ---
class SimpleTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("PowerText Editor")
        self.root.geometry("800x600")

        # --- Text Area ---
        self.text_area = tk.Text(root, wrap="none", undo=True)
        self.text_area.pack(fill="both", expand=True)

        # --- Scrollbars ---
        scroll_y = tk.Scrollbar(self.text_area, orient="vertical", command=self.text_area.yview)
        scroll_y.pack(side="right", fill="y")
        self.text_area.configure(yscrollcommand=scroll_y.set)

        scroll_x = tk.Scrollbar(self.text_area, orient="horizontal", command=self.text_area.xview)
        scroll_x.pack(side="bottom", fill="x")
        self.text_area.configure(xscrollcommand=scroll_x.set)

        # --- Menu Bar ---
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

        # --- Keyboard Shortcuts ---
        root.bind("<Control-n>", lambda e: self.new_file())
        root.bind("<Control-o>", lambda e: self.open_file())
        root.bind("<Control-s>", lambda e: self.save_file())

        # --- Current File ---
        self.file_path = None

    # --- File Functions ---
    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.root.title("PowerText Editor - New File")

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if path:
            with open(path, "r") as file:
                content = file.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, content)
            self.file_path = path
            self.root.title(f"PowerText Editor - {path}")

    def save_file(self):
        if self.file_path is None:
            path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if not path:
                return
            self.file_path = path
        with open(self.file_path, "w") as file:
            content = self.text_area.get(1.0, tk.END)
            file.write(content)
        self.root.title(f"PowerText Editor - {self.file_path}")
        messagebox.showinfo("Saved", "File saved successfully!")

# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleTextEditor(root)
    root.mainloop()
