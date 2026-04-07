import tkinter as tk
from tkinter import messagebox
import json
import os
import sys

def resource_path(relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

def load_level_data(filepath):
    with open(resource_path('levels.json'), 'r') as f:
        data = json.load(f)
    
    level_data = []
    
    for key, value in data.items():
        if '-' in key:
            start, end = map(int, key.split('-'))
            for _ in range(start, end + 1):
                level_data.append(value)
        else:
            level_data.append(value)
    
    return level_data

class ExpCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Level Calculator")
        self.root.geometry("300x200")
        self.reqs = load_level_data('levels.json')

        tk.Label(root, text="Enter Total accumulated EXP:").pack(pady=10)
        self.exp_entry = tk.Entry(root)
        self.exp_entry.pack()
        self.exp_entry.focus_set()
        self.root.bind('<Return>', self.calculate)
        tk.Button(root, text="Calculate Level", command=self.calculate).pack(pady=20)
        self.result_label = tk.Label(root, text="", font=("Arial", 10, "bold"))
        self.result_label.pack()

    def calculate(self, event=None):
        try:
            total_exp = int(self.exp_entry.get())
            current_level = 1
            remaining_exp = total_exp
            pr_gained = 0

            for data in self.reqs[1:]:
                if remaining_exp >= data["cost"]:
                    remaining_exp -= data["cost"]
                    pr_gained += data["pr"]
                    current_level += 1
                else:
                    break
            
            next_level_cost = self.reqs[current_level]["cost"] if current_level < len(self.reqs) else "MAX"
            self.result_label.config(
                text=f"Level: {current_level}\nProgress: {remaining_exp} / {next_level_cost} EXP\nPR's gained: {pr_gained} PR / {3*pr_gained} J"
            )
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpCalculator(root)
    root.mainloop()