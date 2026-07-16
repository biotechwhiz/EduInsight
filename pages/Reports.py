import streamlit as st
import pandas as pd

st.markdown("## 📋 Performance Reports Generator")
st.markdown("Generate specific student academic summaries, alerts, list reports, and download clean data files.")

df = st.session_state["dataset"]

if df is not None:
    # Select report options
    report_type = st.selectbox(
        "Select Report Template",
        [
            "Student Topper Report (Top 10 Leaderboard)",
            "Failed Students Report (Arrears List)",
            "Attendance Warning Report (< 75% Attendance)",
            "Subject-wise Toppers List",
            "Branch / Course Performance Report",
            "Grade Distribution Cohort Summary"
        ]
    )
    
    report_df = pd.DataFrame()
    report_desc = ""
    
    if report_type == "Student Topper Report (Top 10 Leaderboard)":
        report_desc = "### 🏆 Top 10 High Achievers (Sorted by Total Marks)"
        # Sort by total marks descending and take top 10
        report_df = df.sort_values(by="Total", ascending=False).head(10)[
            ["Roll_No", "Student_Name", "Course", "Semester", "Total", "Percentage", "Grade"]
        ]
        
    elif report_type == "Failed Students Report (Arrears List)":
        report_desc = "### ⚠️ Students Requiring Remedial Attention (F Grade)"
        # Filter where Grade is F
        report_df = df[df["Grade"] == "F"][
            ["Roll_No", "Student_Name", "Course", "Semester", "Total", "Percentage", "Grade"]
        ]
        
    elif report_type == "Attendance Warning Report (< 75% Attendance)":
        report_desc = "### 🚨 Attendance Deficit Records (Below 75%)"
        # Filter where Attendance < 75%
        report_df = df[df["Attendance (%)"] < 75.0][
            ["Roll_No", "Student_Name", "Course", "Semester", "Attendance (%)", "Percentage", "Grade"]
        ].sort_values(by="Attendance (%)")
        
    elif report_type == "Subject-wise Toppers List":
        report_desc = "### 🥇 Subject-wise Toppers"
        subjects = ["Python", "Java", "Dot_Net", "PHP", "MERN"]
        toppers = []
        for s in subjects:
            idx = df[s].idxmax()
            top_student = df.loc[idx]
            toppers.append({
                "Subject Domain": s,
                "Topper Roll No": top_student["Roll_No"],
                "Student Name": top_student["Student_Name"],
                "Course": top_student["Course"],
                "Marks Scored": top_student[s],
                "Overall Percentage": f"{top_student['Percentage']}%"
            })
        report_df = pd.DataFrame(toppers)
        
    elif report_type == "Branch / Course Performance Report":
        report_desc = "### 🏫 Course Summary Statistics"
        # Group by course and compute counts and averages
        summary = df.groupby("Course").agg(
            Total_Students=("Roll_No", "count"),
            Average_Percentage=("Percentage", "mean"),
            Highest_Marks=("Total", "max"),
            Lowest_Marks=("Total", "min")
        ).reset_index()
        summary["Average_Percentage"] = summary["Average_Percentage"].round(2)
        
        # Calculate Pass Rate (%) per course
        pass_rates = []
        for course in summary["Course"]:
            course_df = df[df["Course"] == course]
            passed = len(course_df[course_df["Grade"] != "F"])
            rate = (passed / len(course_df)) * 100
            pass_rates.append(round(rate, 2))
        summary["Pass_Rate (%)"] = pass_rates
        report_df = summary
        
    elif report_type == "Grade Distribution Cohort Summary":
        report_desc = "### 📊 Performance Cohort Performance Metrics"
        # Summary details group by grade
        report_df = df.groupby("Grade").agg(
            Student_Count=("Roll_No", "count"),
            Average_Percentage=("Percentage", "mean"),
            Average_Attendance=("Attendance (%)", "mean")
        ).reset_index()
        report_df["Average_Percentage"] = report_df["Average_Percentage"].round(2)
        report_df["Average_Attendance"] = report_df["Average_Attendance"].round(2)
        
    st.markdown("---")
    st.markdown(report_desc)
    
    if report_df.empty:
        st.info("🎉 Excellent news! No students match the failure/warning criteria for this report.")
    else:
        st.write(f"Total matching records: **{len(report_df)}**")
        st.dataframe(report_df, width='stretch', hide_index=True)
        
        # Download Section
        csv_data = report_df.to_csv(index=False).encode('utf-8')
        file_name_formatted = report_type.lower().replace(" ", "_").replace("(", "").replace(")", "") + ".csv"
        
        st.download_button(
            label=f"📥 Download Report ({file_name_formatted})",
            data=csv_data,
            file_name=file_name_formatted,
            mime="text/csv",
            width='stretch'
        )
else:
    st.info("No active dataset. Please upload or load a dataset in the Dataset Management page.")
