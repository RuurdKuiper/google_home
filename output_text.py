import tkinter as tk    

def display_text(self, text):
    self.output_text.config(state="normal")
    # If the user is scrolled down, automatically scroll to bottom
    if self.output_text.yview()[1] == 1.0:
        self.output_text.insert(tk.END, text)  # Insert new text
        self.output_text.see("end")
    else:
        self.output_text.insert(tk.END, text)  # Insert new text
    self.output_text.config(state="disabled")  # Disable editing
