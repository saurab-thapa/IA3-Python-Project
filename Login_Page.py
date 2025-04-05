import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

USERS = {
    "abc": "123",
}


class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Attendance & Performance Analyzer")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self, text="Login", font=("Times New Roman", 30))
        title.pack(pady=20)

        frame = ttk.Frame(self)
        frame.pack(pady=10)

    
        ttk.Label(frame, text="Username:").grid(row=0, column=0, pady=5, sticky="e")
        self.username_entry = ttk.Entry(frame)
        self.username_entry.grid(row=0, column=1, pady=5)

  
        ttk.Label(frame, text="Password:").grid(row=1, column=0, pady=5, sticky="e")
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

       
        login_btn = ttk.Button(self, text="Login", command=self.login)
        login_btn.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in USERS and USERS[username] == password:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.destroy()
            dashboard = DashboardApp(username)
            dashboard.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")


class DashboardApp(tk.Tk):
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
            action_btn = ttk.Button(btn_frame, text=text, width=30)
            action_btn.pack(pady=8)


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
