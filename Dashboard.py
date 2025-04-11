import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from connect import *
import os
from datetime import datetime
from data_preprocessing import *

class BaseDashboard(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.conn = sqlcon()
        self.cursor = self.conn.cursor()

    def take_attendance(self):
        today = datetime.today().strftime('%Y-%m-%d')

        try:
            conn = sqlcon()
            cursor = conn.cursor()

            cursor.execute("SHOW COLUMNS FROM attendance")
            columns = [col[0] for col in cursor.fetchall()]
            if today not in columns:
                cursor.execute(f"ALTER TABLE attendance ADD COLUMN `{today}` VARCHAR(2) DEFAULT 'A'")

            cursor.execute("SELECT id, name FROM attendance")
            details = cursor.fetchall()

            df = pd.DataFrame(details, columns=["ID", "Name"])
            df[today] = 'A'

            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")],title="Save Attendance Sheet")
            if not file_path:
                return
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", f"Attendance sheet saved. Please edit and upload after marking.")

            conn.close()
            self.upload_updated_attendance()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def upload_updated_attendance(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path)
            today = datetime.today().strftime('%Y-%m-%d')

            conn = sqlcon()
            cursor = conn.cursor()

            cursor.execute("SHOW COLUMNS FROM attendance")
            columns = [col[0] for col in cursor.fetchall()]
            if today not in columns:
                cursor.execute(f"ALTER TABLE attendance ADD COLUMN `{today}` VARCHAR(2) DEFAULT 'A'")

            for _, row in df.iterrows():
                sid = row['ID']
                status = row[today]
                cursor.execute(f"UPDATE attendance SET `{today}` = %s WHERE id = %s", (status, sid))

            conn.commit()
            messagebox.showinfo("Success", "Attendance updated successfully from Excel.")
            conn.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))


    def view_performance(self):
        window = tk.Tk()
        app = PredictorGUI(window)
        window.mainloop()

    def export_report(self):
        self.cursor.execute("SELECT * FROM details")
        data = self.cursor.fetchall()

        with open("student_report.csv", "w") as file:
            file.write("ID,Name,Roll Number,Attendance,Marks\n")
            for row in data:
                file.write(",".join(map(str, row)) + "\n")

        messagebox.showinfo("Export", "Report saved as 'student_report.csv'.")

    def logout(self):
        self.destroy()


class DashboardUser(BaseDashboard):
    def __init__(self, username):
        super().__init__(username)
        self.title("Dashboard - Student Analyzer")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        greeting = ttk.Label(self, text=f"Welcome, {self.username}", font=("Times New Roman", 30))
        greeting.pack(pady=15)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        actions = {
            "Enter Attendance": self.take_attendance,
            "View Performance": self.view_performance,
            "Export Report": self.export_report,
            "Logout": self.logout
        }

        for text, command in actions.items():
            ttk.Button(btn_frame, text=text, width=30, command=command).pack(pady=8)


class DashboardAdmin(BaseDashboard):
    def __init__(self, username):
        super().__init__(username)
        self.title("Dashboard - Admin Panel")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        greeting = ttk.Label(self, text=f"Welcome Admin {self.username}", font=("Times New Roman", 30))
        greeting.grid(row=0,column=0,pady=15)

        btn_frame = ttk.Frame(self)
        btn_frame.grid(pady=10)

        actions = {
            "Add New Column to selected table": self.add_column,
            "Add New Student": self.add_student,
            "Enter Attendance": self.take_attendance,
            "View Performance": self.view_performance,      
            "Export Report": self.export_report,            
            "Logout": self.logout                            
        }
        i=1
        for text, command in actions.items():
            ttk.Button(btn_frame, text=text, width=30, command=command).grid(row=i,column=0,pady=8)
            i=i+1


    def add_column(self):
        try:
            self.cursor.execute("ALTER TABLE details ADD COLUMN notes TEXT")
            self.conn.commit()
            messagebox.showinfo("Success", "Column 'notes' added to 'details' table.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_student(self):
        def submit_student():
           student_id = id_entry.get()
           name = name_entry.get()
           attendance = float(attendance_entry.get())
           behavior = behavior_entry.get()
           participation = participation_entry.get()
           absences = int(absences_entry.get())
           final_score = float(final_score_entry.get())

           try:
                self.cursor.execute("""INSERT INTO details (Student_ID, Name, Attendance_Percent, Behavior_Rating, Participation, 
                                    Absences, Final_Exam_Score)      VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
                                    (student_id, name, attendance, behavior, participation, absences, final_score))
    
                self.conn.commit()
           except Exception as e:
                print("Error inserting into database:", e)
        
        window = tk.Toplevel(self)
        window.title("Add Student")

        tk.Label(window, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        name_entry = ttk.Entry(window)
        name_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        tk.Label(window, text="Id Number:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        id_entry = ttk.Entry(window)
        id_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        tk.Label(window, text="Attendance Percent").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        attendance_entry = tk.Entry(window)
        attendance_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(window, text="Behavior Rating").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        behavior_entry = tk.Entry(window)
        behavior_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(window, text="Participation").grid(row=4, column=0, padx=10, pady=5, sticky='w')
        participation_entry = tk.Entry(window)
        participation_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(window, text="Absences").grid(row=5, column=0, padx=10, pady=5, sticky='w')
        absences_entry = tk.Entry(window)
        absences_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(window, text="Final Exam Score").grid(row=6, column=0, padx=10, pady=5, sticky='w')
        final_score_entry = tk.Entry(window)
        final_score_entry.grid(row=6, column=1, padx=10, pady=5)

        ttk.Button(window, text="Add Student", command=submit_student).grid(row=7, column=0, padx=10, pady=5, sticky='w')