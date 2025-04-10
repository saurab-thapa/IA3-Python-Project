import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

df = pd.read_csv(r'C:\Users\bg057\OneDrive\Documents\Python experiments\IA3-Python-Project\student_performance_dataset.csv')

X = df[['Attendance (%)', 'Test 1 Score', 'Test 2 Score', 'Assignment Score', 'Study Hours/Week']]
y = df['Final Result']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(classification_report(y_test, y_pred))