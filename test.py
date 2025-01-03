import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time

def perform_search():
    output_text.delete("1.0", tk.END)
    query = search_entry.get()
    if not query:
        messagebox.showwarning("Input Error", "Please enter a search term.")
        return

    progress_bar.start()
    root.after(1000, lambda: display_result(query))

def display_result(query):
    progress_bar.stop()
    # Simulated search result
    result = f"You searched for: {query}\nResult: This is a simulated response."
    output_text.insert(tk.END, result)

# Initialize main window
root = tk.Tk()
root.title("Search Application")
root.geometry("600x400")

# Dark theme styling
root.configure(bg="#2e2e2e")
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#2e2e2e", foreground="#ffffff")
style.configure("TButton", background="#444444", foreground="#ffffff")
style.map("TButton", background=[("active", "#555555")])
style.configure("TProgressbar", background="#00ff00")

# Search input and button frame
frame_top = tk.Frame(root, bg="#2e2e2e")
frame_top.pack(pady=20)

search_label = ttk.Label(frame_top, text="Enter Search Query:")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = ttk.Entry(frame_top, width=40)
search_entry.pack(side=tk.LEFT, padx=5)

search_button = ttk.Button(frame_top, text="Search", command=perform_search)
search_button.pack(side=tk.LEFT, padx=5)

# Output text area
output_text = tk.Text(root, wrap=tk.WORD, height=15, width=70, bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff", relief=tk.FLAT)
output_text.pack(pady=10, padx=10)

# Progress bar
progress_bar = ttk.Progressbar(root, mode="indeterminate", length=300)
progress_bar.pack(pady=10)

# Run the application
root.mainloop()
