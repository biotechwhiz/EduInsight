import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.markdown("## 🔍 Search Student")
st.markdown("Look up individual student profiles and review their subject-wise grades compared to their course average.")

df = st.session_state["dataset"]

if df is not None:
    # Search controls
    search_col1, search_col2 = st.columns(2)
    
    with search_col1:
        search_type = st.radio("Search by:", ["Roll Number", "Student Name"], horizontal=True)
        
    selected_student = None
    
    with search_col2:
        if search_type == "Roll Number":
            # Generate sorted list of roll numbers
            roll_nos = sorted(df["Roll_No"].unique())
            selected_roll = st.selectbox("Select Roll Number", roll_nos, index=None, placeholder="Search or select a Roll Number...")
            if selected_roll:
                selected_student = df[df["Roll_No"] == selected_roll].iloc[0]
        else:
            # Generate sorted list of names
            names = sorted(df["Student_Name"].unique())
            selected_name = st.selectbox("Select Student Name", names, index=None, placeholder="Search or select a Student Name...")
            if selected_name:
                selected_student = df[df["Student_Name"] == selected_name].iloc[0]

    if selected_student is not None:
        st.markdown("---")
        
        col_profile, col_chart = st.columns([1, 1.2])
        
        with col_profile:
            st.markdown(f"### 👤 Profile: {selected_student['Student_Name']}")
            
            # Grade styling color based on performance
            grade = selected_student['Grade']
            if grade in ['A+', 'A']:
                grade_color = "#2ed573" # Green
            elif grade in ['B', 'C']:
                grade_color = "#ffa502" # Orange/Gold
            elif grade in ['D']:
                grade_color = "#eccc68" # Yellow
            else:
                grade_color = "#ff4757" # Red
                
            st.markdown(
                f"""
                <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; padding: 22px;'>
                    <table style='width:100%; border-collapse:collapse; color:#e0e0e0; font-family:"Outfit",sans-serif; font-size:1.05rem;'>
                        <tr style='border-bottom:1px solid rgba(255,255,255,0.05);'><td style='padding:12px 0; font-weight:600; color:#a0a0a0;'>Roll Number</td><td style='text-align:right; font-weight:700;'>{selected_student['Roll_No']}</td></tr>
                        <tr style='border-bottom:1px solid rgba(255,255,255,0.05);'><td style='padding:12px 0; font-weight:600; color:#a0a0a0;'>Course / Branch</td><td style='text-align:right; font-weight:700;'>{selected_student['Course']}</td></tr>
                        <tr style='border-bottom:1px solid rgba(255,255,255,0.05);'><td style='padding:12px 0; font-weight:600; color:#a0a0a0;'>Semester</td><td style='text-align:right;'>{selected_student['Semester']}</td></tr>
                        <tr style='border-bottom:1px solid rgba(255,255,255,0.05);'><td style='padding:12px 0; font-weight:600; color:#a0a0a0;'>Gender</td><td style='text-align:right;'>{selected_student['Gender']}</td></tr>
                        <tr style='border-bottom:1px solid rgba(255,255,255,0.05);'><td style='padding:12px 0; font-weight:600; color:#a0a0a0;'>Attendance</td><td style='text-align:right; font-weight:700;'>{selected_student['Attendance (%)']}%</td></tr>
                        <tr style='border-bottom:1px solid rgba(255,255,255,0.05);'><td style='padding:12px 0; font-weight:600; color:#a0a0a0;'>Total Score</td><td style='text-align:right; font-weight:700;'>{selected_student['Total']} / 500</td></tr>
                        <tr style='border-bottom:1px solid rgba(255,255,255,0.05);'><td style='padding:12px 0; font-weight:600; color:#a0a0a0;'>Percentage</td><td style='text-align:right; font-weight:700;'>{selected_student['Percentage']}%</td></tr>
                        <tr><td style='padding:12px 0; font-weight:600; color:#a0a0a0;'>Final Grade</td><td style='text-align:right; font-weight:800; font-size:1.3rem; color:{grade_color};'>{grade}</td></tr>
                    </table>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Show status badge below profile
            st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
            if grade == 'F':
                st.markdown("<div style='text-align:center;'><span class='fail-badge'>🔴 FAILURE RECORDED - ACADEMIC SUPPORT REQUIRED</span></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='text-align:center;'><span class='pass-badge'>🟢 PASSED - SATISFACTORY PERFORMANCE</span></div>", unsafe_allow_html=True)
                
        with col_chart:
            st.markdown("### 📊 Subject-wise Performance Comparison")
            
            subjects = ["Python", "Java", "Dot_Net", "PHP", "MERN"]
            student_scores = [selected_student[s] for s in subjects]
            
            # Get average scores of all students in the same course
            course_avg_scores = df[df["Course"] == selected_student["Course"]][subjects].mean().round(1).tolist()
            
            # Grouped bar chart using Plotly graph objects
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=subjects,
                y=student_scores,
                name=selected_student["Student_Name"],
                marker_color='#764ba2'
            ))
            fig.add_trace(go.Bar(
                x=subjects,
                y=course_avg_scores,
                name=f"{selected_student['Course']} Average",
                marker_color='rgba(255, 255, 255, 0.25)'
            ))
            
            fig.update_layout(
                barmode='group',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#d0d0d0', family='Outfit'),
                yaxis=dict(
                    gridcolor='rgba(255,255,255,0.05)',
                    range=[0, 105],
                    title="Marks Obtained"
                ),
                margin=dict(l=20, r=20, t=30, b=20),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Custom Diagnostic Analysis Report
            st.markdown("##### 💡 Academic Diagnostics Advice")
            
            # Compute weak/strong areas
            min_score = min(student_scores)
            min_sub = subjects[student_scores.index(min_score)]
            max_score = max(student_scores)
            max_sub = subjects[student_scores.index(max_score)]
            
            feedback_messages = []
            
            # Attendance check
            if selected_student["Attendance (%)"] < 75:
                feedback_messages.append(f"⚠️ **Low Attendance Alert:** Student's attendance is **{selected_student['Attendance (%)']}%** (minimum recommended: 75%). Low attendance is correlated with decreased score efficiency.")
            
            # Strengths
            feedback_messages.append(f"🌟 **Core Strength:** Performing exceptionally well in **{max_sub}** with a top score of **{max_score}**.")
            
            # Weakness checks
            if min_score < 50:
                feedback_messages.append(f"🚨 **Urgent Action Required:** Score in **{min_sub}** is failing ({min_score} marks). Recommend enrollment in remedial sessions or tutor assignment.")
            elif min_score < 65:
                feedback_messages.append(f"📉 **Area of Improvement:** Performance in **{min_sub}** ({min_score} marks) is lagging behind expectations. Recommend supplementary coursework.")
            else:
                feedback_messages.append(f"🏆 **All-Round Performance:** Maintaining healthy performance across all domains. Keep up the consistency.")
                
            for msg in feedback_messages:
                st.markdown(f"- {msg}")
else:
    st.info("No active dataset. Please upload or load a dataset in the Dataset Management page.")
