import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class DashboardUser(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.title("Dashboard - Student Analyzer",)
        self.geometry("600x400")
        self.username = username

        self.create_widgets()

    def create_widgets(self):
        greeting = ttk.Label(self, text=f"Welcome, {self.username}", font=("Times New Roman", 30))
        greeting.pack(pady=15)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        buttons = [
            "Enter Attendance",
            "View Performance",
            "Export Report",
            "Logout"
        ]

        for text in buttons:
            attend_btn = ttk.Button(btn_frame, text=text, width=30)
            attend_btn.pack(pady=8)

class DashboardAdmin(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.title("Dashboard - Student Analyzer",)
        self.geometry("800x600")
        self.username = username

        self.create_widgets()

    def create_widgets(self):
        greeting = ttk.Label(self, text=f"Welcome, {self.username}", font=("Times New Roman", 30))
        greeting.pack(pady=15)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        buttons = [
            "Add New Table"
            "Add New Column to selected table"
            "Add New Student"
            "Enter Attendance",
            "View Performance",
            "Export Report",
            "Logout"
        ]

        for text in buttons:
            action_btn = ttk.Button(btn_frame, text=text, width=30)
            action_btn.pack(pady=8)