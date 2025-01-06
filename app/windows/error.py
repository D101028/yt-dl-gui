import tkinter as tk
from tkinter import messagebox

class ErrorWindow:
    def __init__(self, error_message):
        self.error_message = error_message
        self.create_error_window()

    def create_error_window(self):
        messagebox.showerror("Error", self.error_message)


