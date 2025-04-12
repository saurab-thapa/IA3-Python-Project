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

            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel Files", "*.xlsx")],
                title="Save Attendance Sheet"
            )
            if not file_path:
                return

            df.to_excel(file_path, index=False)
            messagebox.showinfo("Attendance Sheet Saved", 
                                f"Attendance sheet saved to:\n{file_path}\n\nPlease open the file and update attendance (P/A).")

            response = messagebox.askyesno("Upload Attendance?",
                                        "Have you finished marking the attendance in the Excel sheet?\nClick YES to proceed with upload.")

            if response:
                self.upload_updated_attendance()
            else:
                messagebox.showinfo("Reminder", "You can upload the attendance later from the dashboard.")

            conn.close()

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
        self.geometry("500x400")
        self.create_widgets()

    def create_widgets(self):
        greeting = ttk.Label(self, text=f"Welcome, {self.username}", font=("Times New Roman", 30))
        greeting.pack(pady=15)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        actions = {
            "Enter Attendance": self.take_attendance,
            "Upload Attendance": self.upload_updated_attendance,
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
        self.geometry("500x400")
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
            "Upload Attendance": self.upload_updated_attendance,
            "View Performance": self.view_performance,
            "Export Report": self.export_report,
            "Logout": self.logout
        }

        i=1
        for text, command in actions.items():
            ttk.Button(btn_frame, text=text, width=30, command=command).grid(row=i,column=0,pady=8)
            i=i+1


    def add_column(self):
        def submit_column():
            table = table_entry.get()
            column = column_entry.get()
            col_type = type_var.get() or "TEXT"

            if not table or not column:
                messagebox.showwarning("Input Error", "Please enter both table and column name.")
                return

            try:
                self.cursor.execute(f"ALTER TABLE `{table}` ADD COLUMN `{column}` {col_type}")
                self.conn.commit()
                messagebox.showinfo("Success", f"Column '{column}' added to '{table}' table.")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        window = tk.Toplevel(self)
        window.title("Add New Column")

        tk.Label(window, text="Table Name:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        table_entry = ttk.Entry(window)
        table_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(window, text="Column Name:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        column_entry = ttk.Entry(window)
        column_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(window, text="Column Type:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        type_var = tk.StringVar(value="TEXT")
        type_options = ["TEXT", "VARCHAR(255)", "INT", "FLOAT", "DATE"]
        ttk.Combobox(window, textvariable=type_var, values=type_options).grid(row=2, column=1, padx=10, pady=5)

        ttk.Button(window, text="Add Column", command=submit_column).grid(row=3, column=0, columnspan=2, pady=10)

    def add_student(self):
        def submit_student():
            try:
                if not id_entry.get() or not name_entry.get():
                    raise ValueError("Student ID and Name are required.")

                if gender_var.get() not in ("Male", "Female"):
                    raise ValueError("Please select a valid Gender.")

                if internet_var.get() not in ("Yes", "No") or coaching_var.get() not in ("Yes", "No"):
                    raise ValueError("Please select Yes or No for Internet and Coaching.")

                if result_var.get() not in ("Pass", "Fail"):
                    raise ValueError("Please select Pass or Fail for Final Result.")

                data = (
                    id_entry.get(),
                    name_entry.get(),
                    gender_var.get(),
                    int(age_entry.get()),
                    float(attendance_entry.get()),
                    float(test1_entry.get()),
                    float(test2_entry.get()),
                    float(assignment_entry.get()),
                    float(study_hours_entry.get()),
                    parent_edu_entry.get(),
                    internet_var.get(),
                    coaching_var.get(),
                    behavior_entry.get(),
                    participation_entry.get(),
                    int(absences_entry.get()),
                    float(final_score_entry.get()),
                    result_var.get()
                )

                self.cursor.execute("""
                    INSERT INTO details (
                        Student_ID, Name, Gender, Age, Attendance_Percent, Test1_Score, Test2_Score,
                        Assignment_Score, Study_Hours_Per_Week, Parent_Education, Internet_Access,
                        Extra_Coaching, Behavior_Rating, Participation, Absences,
                        Final_Exam_Score, Final_Result
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, data)

                self.conn.commit()
                messagebox.showinfo("Success", "Student added successfully.")
                window.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Error adding student:\n{e}")
                
        window = tk.Toplevel(self)
        window.title("Add New Student")

        tk.Label(window, text="Student ID").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        id_entry = ttk.Entry(window)
        id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(window, text="Name").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        name_entry = ttk.Entry(window)
        name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(window, text="Gender").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        gender_var = tk.StringVar()
        ttk.Radiobutton(window, text="Male", variable=gender_var, value="Male").grid(row=2, column=1, sticky='w')
        ttk.Radiobutton(window, text="Female", variable=gender_var, value="Female").grid(row=2, column=1, sticky='e')

        tk.Label(window, text="Age").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        age_entry = ttk.Entry(window)
        age_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(window, text="Attendance (%)").grid(row=4, column=0, padx=10, pady=5, sticky='w')
        attendance_entry = ttk.Entry(window)
        attendance_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(window, text="Test 1 Score").grid(row=5, column=0, padx=10, pady=5, sticky='w')
        test1_entry = ttk.Entry(window)
        test1_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(window, text="Test 2 Score").grid(row=6, column=0, padx=10, pady=5, sticky='w')
        test2_entry = ttk.Entry(window)
        test2_entry.grid(row=6, column=1, padx=10, pady=5)

        tk.Label(window, text="Assignment Score").grid(row=7, column=0, padx=10, pady=5, sticky='w')
        assignment_entry = ttk.Entry(window)
        assignment_entry.grid(row=7, column=1, padx=10, pady=5)

        tk.Label(window, text="Study Hours/Week").grid(row=8, column=0, padx=10, pady=5, sticky='w')
        study_hours_entry = ttk.Entry(window)
        study_hours_entry.grid(row=8, column=1, padx=10, pady=5)

        tk.Label(window, text="Parent Education").grid(row=9, column=0, padx=10, pady=5, sticky='w')
        parent_edu_entry = ttk.Entry(window)
        parent_edu_entry.grid(row=9, column=1, padx=10, pady=5)

        tk.Label(window, text="Internet Access").grid(row=10, column=0, padx=10, pady=5, sticky='w')
        internet_var = tk.StringVar()
        internet_dropdown = ttk.OptionMenu(window, internet_var, "Yes", "Yes", "No")
        internet_dropdown.grid(row=10, column=1, padx=10, pady=5)

        tk.Label(window, text="Extra Coaching").grid(row=11, column=0, padx=10, pady=5, sticky='w')
        coaching_var = tk.StringVar()
        coaching_dropdown = ttk.OptionMenu(window, coaching_var, "No", "Yes", "No")
        coaching_dropdown.grid(row=11, column=1, padx=10, pady=5)

        tk.Label(window, text="Behavior Rating").grid(row=12, column=0, padx=10, pady=5, sticky='w')
        behavior_entry = ttk.Entry(window)
        behavior_entry.grid(row=12, column=1, padx=10, pady=5)

        tk.Label(window, text="Participation").grid(row=13, column=0, padx=10, pady=5, sticky='w')
        participation_entry = ttk.Entry(window)
        participation_entry.grid(row=13, column=1, padx=10, pady=5)

        tk.Label(window, text="Absences").grid(row=14, column=0, padx=10, pady=5, sticky='w')
        absences_entry = ttk.Entry(window)
        absences_entry.grid(row=14, column=1, padx=10, pady=5)

        tk.Label(window, text="Final Exam Score").grid(row=15, column=0, padx=10, pady=5, sticky='w')
        final_score_entry = ttk.Entry(window)
        final_score_entry.grid(row=15, column=1, padx=10, pady=5)

        tk.Label(window, text="Final Result").grid(row=16, column=0, padx=10, pady=5, sticky='w')
        result_var = tk.StringVar()
        result_dropdown = ttk.OptionMenu(window, result_var, "Pass", "Pass", "Fail")
        result_dropdown.grid(row=16, column=1, padx=10, pady=5)

        ttk.Button(window, text="Add Student", command=submit_student).grid(row=17, column=0, columnspan=2, pady=15)

        

