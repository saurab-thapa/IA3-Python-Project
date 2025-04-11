USE students;
INSERT INTO details (Student_ID, Name, Attendance_Percent, Behavior_Rating, Participation, Absences, Final_Exam_Score,Final_Result)
VALUES 
('S019', 'Student_19', 52.86, 'Good', 'Yes', 2, 100.00,'Fail'),
('S020', 'Student_20', 81.14, 'Poor', 'Yes', 1, 78.00,'Fail'),
('S021', 'Student_21', 68.86, 'Average', 'Yes', 0, 76.00,'Fail'),
('S022', 'Student_22', 91.43, 'Good', 'Yes', 0, 94.00,'Fail'),
('S023', 'Student_23', 89.14, 'Good', 'Yes', 0, 92.30,'Fail'),
('S024', 'Student_24', 81.71, 'Poor', 'No', 0, 70.70,'Fail'),
('S025', 'Student_25', 82.00, 'Average', 'No', 1, 80.00,'Fail'),
('S026', 'Student_26', 90.00, 'Good', 'Yes', 1, 88.00,'Fail'),
('S027', 'Student_27', 77.14, 'Good', 'Yes', 1, 85.00,'Fail'),
('S028', 'Student_28', 62.86, 'Poor', 'Yes', 1, 68.00,'Fail') AS new
ON DUPLICATE KEY UPDATE
    Name = new.Name,
    Attendance_Percent = new.Attendance_Percent,
    Behavior_Rating = new.Behavior_Rating,
    Participation = new.Participation,
    Absences = new.Absences,
    Final_Exam_Score = new.Final_Exam_Score;

select * from details;