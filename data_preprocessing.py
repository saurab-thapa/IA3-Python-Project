import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from connect import * 

def fetch_details_data():
    try:
        conn = sqlcon()
        query = "SELECT * FROM details"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred while fetching data: {e}")
        return pd.DataFrame() 

def train_model():
    df = fetch_details_data()
    df = df.dropna()
    if df.empty:
        return pd.DataFrame()
    label_cols = ['Name', 'Gender', 'Parent_Education', 'Internet_Access',
                  'Extra_Coaching', 'Behavior_Rating', 'Participation', 'Final_Result']
    le = LabelEncoder()
    for col in label_cols:
        df[col] = le.fit_transform(df[col])

    X = df.drop(columns=['Student_ID', 'Name', 'Final_Result'])
    y = df['Final_Result']

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    df['Predicted_Result'] = model.predict(X)
    df['Predicted_Result'] = df['Predicted_Result'].apply(lambda x: "Pass" if x == 1 else "Fail")

    return df[['Student_ID', 'Name', 'Predicted_Result']]

class PredictorGUI:
    def __init__(self, windowp):
        self.windowp = windowp
        self.windowp.title("Student Performance Predictor")
        self.windowp.geometry("600x400")

        title = tk.Label(windowp, text="Predict Student Final Results", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        self.button = tk.Button(windowp, text="Predict", command=self.show_predictions)
        self.button.pack(pady=10)

        self.tree = ttk.Treeview(windowp, columns=("ID", "Name", "Result"), show='headings')
        self.tree.heading("ID", text="Student ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Result", text="Predicted_Result")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def show_predictions(self):
        data = train_model()
        if data.empty:
            messagebox.showerror("No Data", "No data available or an error occurred.")
            return
        
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for _, row in data.iterrows():
            self.tree.insert('', tk.END, values=(row['Student_ID'], row['Name'], row['Predicted_Result']))


