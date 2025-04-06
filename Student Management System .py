

import tkinter as tk
from tkinter import messagebox, ttk
import os

# ------------------ Student Class ------------------
class Student:
    def __init__(self, student_id, name, age, marks):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.marks = marks

    def __str__(self):
        return f"{self.student_id}, {self.name}, {self.age}, {self.marks}"

# ------------------ Storage ------------------
students = []
student_ids = set()
student_dict = {}

# ------------------ Functions ------------------
def add_student():
    sid = id_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    marks = marks_entry.get()

    if not (sid and name and age and marks):
        messagebox.showwarning("⚠️ Input Error", "All fields are required.")
        return

    if sid in student_ids:
        messagebox.showerror("❌ Duplicate ID", "Student ID already exists.")
        return

    try:
        age = int(age)
        marks = float(marks)
    except ValueError:
        messagebox.showerror("🚫 Input Error", "Age must be int, Marks must be float.")
        return

    student = Student(sid, name, age, marks)
    students.append(student)
    student_ids.add(sid)
    student_dict[sid] = student

    messagebox.showinfo("✅ Success", "Student added successfully!")
    clear_fields()
    view_students()

def clear_fields():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)

def view_students():
    listbox.delete(*listbox.get_children())
    for s in students:
        listbox.insert('', 'end', values=(s.student_id, s.name, s.age, s.marks))

def search_student():
    sid = id_entry.get()
    student = student_dict.get(sid)
    if student:
        messagebox.showinfo("📘 Student Found", str(student))
    else:
        messagebox.showerror("😢 Not Found", "Student ID not found.")

def save_students():
    with open("students_gui.txt", "w") as f:
        for s in students:
            f.write(f"{s.student_id},{s.name},{s.age},{s.marks}\n")
    messagebox.showinfo("💾 Saved", "Students saved to students_gui.txt")

def load_students():
    if not os.path.exists("students_gui.txt"):
        return
    with open("students_gui.txt", "r") as f:
        for line in f:
            sid, name, age, marks = line.strip().split(",")
            if sid not in student_ids:
                student = Student(sid, name, int(age), float(marks))
                students.append(student)
                student_ids.add(sid)
                student_dict[sid] = student
    view_students()

# ------------------ GUI Setup ------------------
root = tk.Tk()
root.title("🎓 Student Management System")
root.geometry("750x550")
root.configure(bg="#f0f8ff")

# Style
style = ttk.Style()
style.configure("Treeview", background="#ffffff", foreground="black", rowheight=25, fieldbackground="#f9f9f9")
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.map("TButton", foreground=[('active', '#ffffff')], background=[('active', '#007acc')])

# Labels & Inputs
tk.Label(root, text="Student ID:", font=("Segoe UI", 10), bg="#f0f8ff").grid(row=0, column=0, sticky="e", padx=10, pady=5)
tk.Label(root, text="Name:", font=("Segoe UI", 10), bg="#f0f8ff").grid(row=1, column=0, sticky="e", padx=10, pady=5)
tk.Label(root, text="Age:", font=("Segoe UI", 10), bg="#f0f8ff").grid(row=2, column=0, sticky="e", padx=10, pady=5)
tk.Label(root, text="Marks:", font=("Segoe UI", 10), bg="#f0f8ff").grid(row=3, column=0, sticky="e", padx=10, pady=5)

entry_style = {"font": ("Segoe UI", 10), "bd": 2, "relief": "groove", "width": 25}
id_entry = tk.Entry(root, **entry_style)
name_entry = tk.Entry(root, **entry_style)
age_entry = tk.Entry(root, **entry_style)
marks_entry = tk.Entry(root, **entry_style)

id_entry.grid(row=0, column=1, pady=5)
name_entry.grid(row=1, column=1, pady=5)
age_entry.grid(row=2, column=1, pady=5)
marks_entry.grid(row=3, column=1, pady=5)

# Buttons
button_style = {"width": 15}
ttk.Button(root, text="➕ Add Student", command=add_student).grid(row=0, column=2, padx=10)
ttk.Button(root, text="🔍 Search", command=search_student).grid(row=1, column=2, padx=10)
ttk.Button(root, text="📋 View All", command=view_students).grid(row=2, column=2, padx=10)
ttk.Button(root, text="💾 Save", command=save_students).grid(row=3, column=2, padx=10)
ttk.Button(root, text="🧹 Clear", command=clear_fields).grid(row=4, column=1, pady=10)

# TreeView for table
cols = ("ID", "Name", "Age", "Marks")
listbox = ttk.Treeview(root, columns=cols, show="headings", height=10)
for col in cols:
    listbox.heading(col, text=col)
    listbox.column(col, anchor=tk.CENTER)

# Scrollbar
scrollbar = ttk.Scrollbar(root, orient="vertical", command=listbox.yview)
listbox.configure(yscrollcommand=scrollbar.set)
listbox.grid(row=6, column=0, columnspan=3, padx=15, pady=10)
scrollbar.grid(row=6, column=3, sticky="ns")

# Load data
load_students()

# Run app
root.mainloop()
