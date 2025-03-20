import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

# Database Setup
conn = sqlite3.connect("python_learning.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        option1 TEXT,
        option2 TEXT,
        option3 TEXT,
        correct TEXT
    )
""")
conn.commit()

# Sample Questions
sample_questions = [
    ("What is the output of print(2**3)?", "6", "8", "10", "8"),
    ("Which keyword is used to define a function?", "define", "def", "func", "def"),
    ("Which data type is mutable in Python?", "Tuple", "String", "List", "List")
]

# Insert Sample Questions (only if DB is empty)
cursor.execute("SELECT COUNT(*) FROM questions")
if cursor.fetchone()[0] == 0:
    cursor.executemany("INSERT INTO questions (question, option1, option2, option3, correct) VALUES (?, ?, ?, ?, ?)", sample_questions)
    conn.commit()

# App GUI
class PythonLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Learning App")
        self.root.geometry("400x300")
        
        self.label = tk.Label(root, text="Python Memorization Quiz", font=("Arial", 14))
        self.label.pack(pady=10)
        
        self.question_label = tk.Label(root, text="", wraplength=380, font=("Arial", 12))
        self.question_label.pack(pady=5)
        
        self.options = []
        for i in range(3):
            btn = tk.Button(root, text="", font=("Arial", 10), command=lambda i=i: self.check_answer(i))
            btn.pack(pady=2, fill=tk.X)
            self.options.append(btn)
        
        self.next_button = tk.Button(root, text="Next", font=("Arial", 12), command=self.load_question)
        self.next_button.pack(pady=10)
        
        self.score = 0
        self.load_question()

    def load_question(self):
        self.question = random.choice(cursor.execute("SELECT * FROM questions").fetchall())
        self.question_label.config(text=self.question[1])
        for i in range(3):
            self.options[i].config(text=self.question[i+2])

    def check_answer(self, index):
        selected_option = self.options[index].cget("text")
        if selected_option == self.question[5]:
            self.score += 1
            messagebox.showinfo("Correct!", f"Good job! Your score: {self.score}")
        else:
            messagebox.showerror("Wrong!", f"Correct answer: {self.question[5]}")
        self.load_question()

# Run the App
root = tk.Tk()
app = PythonLearningApp(root)
root.mainloop()
