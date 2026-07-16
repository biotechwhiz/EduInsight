import os
import pandas as pd
import numpy as np

# Ensure directory exists
os.makedirs("C:/Users/ACS/.gemini/antigravity/scratch/EduInsight/data", exist_ok=True)

# Generate mock dataset of 120 students
np.random.seed(42)

roll_nos = list(range(101, 221))
names = [
    "Rahul Sharma", "Priya Singh", "Aman Verma", "Sneha Patel", "Amit Kumar",
    "Anjali Gupta", "Rohan Mehta", "Neha Reddy", "Vikram Malhotra", "Divya Nair",
    "Siddharth Rao", "Kirti Sharma", "Aditya Sen", "Pooja Bose", "Rajesh Yadav",
    "Swati Mishra", "Karan Johar", "Ritu Jain", "Sanjay Dutt", "Meera Sen",
    "Abhishek Bachchan", "Kareena Kapoor", "Hrithik Roshan", "Deepika Padukone", "Ranbir Kapoor",
    "Alia Bhatt", "Varun Dhawan", "Shraddha Kapoor", "Arjun Kapoor", "Parineeti Chopra",
    "Sidharth Malhotra", "Kiara Advani", "Kartik Aaryan", "Sara Ali Khan", "Janhvi Kapoor",
    "Ishaan Khatter", "Ananya Panday", "Vijay Deverakonda", "Rashmika Mandanna", "Samantha Ruth",
    "Nani Rao", "Prabhas Raju", "Allu Arjun", "Ram Charan", "NTR Junior",
    "Mahesh Babu", "Pawan Kalyan", "Ravi Teja", "Nagarjuna Akkineni", "Venkatesh Daggubati",
    "Dulquer Salmaan", "Fahadh Faasil", "Nivin Pauly", "Tovino Thomas", "Prithviraj Sukumaran",
    "Mohanlal Viswanathan", "Mammootty Kutty", "Yash Gowda", "Sudeep Sanjeev", "Darshan Thoogudeepa",
    "Puneeth Rajkumar", "Shiva Rajkumar", "Upendra Rao", "Rakshit Shetty", "Rishab Shetty",
    "John Abraham", "Bipasha Basu", "Emraan Hashmi", "Vidya Balan", "Rani Mukerji",
    "Preity Zinta", "Aishwarya Rai", "Salman Khan", "Aamir Khan", "Shah Rukh Khan",
    "Saif Ali Khan", "Karisma Kapoor", "Madhuri Dixit", "Sridevi Kapoor", "Juhi Chawla",
    "Kajol Devgan", "Tabassum Hashmi", "Sushmita Sen", "Lara Dutta", "Dia Mirza",
    "Priyanka Chopra", "Katrina Kaif", "Anushka Sharma", "Sonam Kapoor", "Jacqueline Fernandez",
    "Nushrratt Bharuccha", "Bhumi Pednekar", "Taapsee Pannu", "Yami Gautam", "Kriti Sanon",
    "Tara Sutaria", "Disha Patani", "Rakul Preet", "Mrunal Thakur", "Wamiqa Gabbi",
    "Sobhita Dhulipala", "Aditi Rao", "Huma Qureshi", "Radhika Apte", "Konkona Sen",
    "Richa Chadha", "Kalki Koechlin", "Nimrat Kaur", "Sanya Malhotra", "Fatima Sana",
    "Radhika Madan", "Sharvari Wagh", "Alaya Furniturewalla", "Manushi Chhillar", "Shehnaaz Gill",
    "Tejasswi Prakash", "Rashami Desai", "Devoleena Bhattacharjee", "Rubina Dilaik", "Jasmin Bhasin"
]

# Truncate or pad names to exactly 120
if len(names) < 120:
    names = names * 2
names = names[:120]

genders = np.random.choice(["Male", "Female"], size=120, p=[0.55, 0.45])
courses = np.random.choice(["BCA", "B.Tech", "MCA", "Diploma"], size=120, p=[0.3, 0.4, 0.2, 0.1])
semesters = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8], size=120)

# Realistic attendance between 55% and 100%
attendance = np.round(np.random.uniform(55.0, 100.0, size=120), 2)

# Marks generation
# Python, Java, Dot_Net, PHP, MERN
python_marks = np.random.randint(40, 100, size=120)
java_marks = np.random.randint(40, 100, size=120)
dotnet_marks = np.random.randint(40, 100, size=120)
php_marks = np.random.randint(40, 100, size=120)
mern_marks = np.random.randint(40, 100, size=120)

# Calculate totals and percentages
totals = python_marks + java_marks + dotnet_marks + php_marks + mern_marks
percentages = np.round((totals / 500) * 100, 2)

# Assign grades
grades = []
for p in percentages:
    if p >= 90:
        grades.append("A+")
    elif p >= 80:
        grades.append("A")
    elif p >= 70:
        grades.append("B")
    elif p >= 60:
        grades.append("C")
    elif p >= 50:
        grades.append("D")
    else:
        grades.append("F")

# Build DataFrame
df = pd.DataFrame({
    "Roll_No": roll_nos,
    "Student_Name": names,
    "Gender": genders,
    "Course": courses,
    "Semester": semesters,
    "Attendance (%)": attendance,
    "Python": python_marks,
    "Java": java_marks,
    "Dot_Net": dotnet_marks,
    "PHP": php_marks,
    "MERN": mern_marks,
    "Total": totals,
    "Percentage": percentages,
    "Grade": grades
})

# Save to CSV
df.to_csv("C:/Users/ACS/.gemini/antigravity/scratch/EduInsight/data/students.csv", index=False)

# Save to XLSX
df.to_excel("C:/Users/ACS/.gemini/antigravity/scratch/EduInsight/data/students.xlsx", index=False)

print("Mock data generated successfully!")
