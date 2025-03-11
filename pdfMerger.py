import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
import os

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("500x400")
        self.files = []

        # Main frame
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # File list
        self.listbox = tk.Listbox(main_frame, selectmode=tk.SINGLE, height=10, bg="white", relief=tk.GROOVE, bd=2)
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)

        # File buttons
        tk.Button(button_frame, text="Add PDFs", command=self.add_files, width=12).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Remove Selected", command=self.remove_file, width=12).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Clear List", command=self.clear_list, width=12).grid(row=0, column=2, padx=5, pady=5)

        # Order buttons
        tk.Button(button_frame, text="Move Up", command=self.move_up, width=12).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Move Down", command=self.move_down, width=12).grid(row=1, column=1, padx=5, pady=5)

        # Merge button
        merge_button = tk.Button(main_frame, text="Merge PDFs", command=self.merge_files, width=20, bg="green", fg="white", font=("Arial", 12, "bold"))
        merge_button.pack(pady=10)

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file in files:
            if file not in self.files:
                self.files.append(file)
                self.listbox.insert(tk.END, os.path.basename(file))

    def remove_file(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.listbox.delete(index)
            self.files.pop(index)

    def clear_list(self):
        self.listbox.delete(0, tk.END)
        self.files = []

    def move_up(self):
        selected_index = self.listbox.curselection()
        if selected_index and selected_index[0] > 0:
            index = selected_index[0]
            self.files[index], self.files[index-1] = self.files[index-1], self.files[index]
            self.update_listbox(index, index-1)

    def move_down(self):
        selected_index = self.listbox.curselection()
        if selected_index and selected_index[0] < len(self.files) - 1:
            index = selected_index[0]
            self.files[index], self.files[index+1] = self.files[index+1], self.files[index]
            self.update_listbox(index, index+1)

    def update_listbox(self, old_index, new_index):
        item = self.listbox.get(old_index)
        self.listbox.delete(old_index)
        self.listbox.insert(new_index, item)
        self.listbox.selection_set(new_index)

    def merge_files(self):
        if not self.files:
            messagebox.showwarning("No files", "No PDF files added")
            return

        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not output_file:
            return

        merger = PdfMerger()
        for file in self.files:
            merger.append(file)

        merger.write(output_file)
        merger.close()
        messagebox.showinfo("Success", "PDFs merged successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
