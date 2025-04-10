import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from connect import *
from Dashboard import *

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
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.access_level=self.verify()

        if self.access_level==1:
            messagebox.showinfo("Login Successful", f"Welcome, {self.username}!")
            self.destroy()
            dashboard = DashboardUser(self.username)
            dashboard.mainloop()
        elif self.access_level==0:
            messagebox.showinfo("Login Successful", f"Welcome, {self.username}!")
            self.destroy()
            dashboard = DashboardUser(self.username)
            dashboard.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def verify(self):
        conn = sqlcon()
        cursor = conn.cursor()
        cursor.execute("SELECT access_level FROM users WHERE username=%s AND pass=%s", (self.username, self.password))
        result = cursor.fetchone()
        conn.close()
        print(result)
        if result == None:
            return 3
        elif result[0]=="Admin":
            return 0
        else:
            return 1
        


app = LoginApp()
app.mainloop()
