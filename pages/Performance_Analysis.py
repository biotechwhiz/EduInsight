import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.markdown("## 📈 Performance Analysis Dashboard")
st.markdown("Review macro-level academic performance metrics, distributions, and correlations using interactive data science visuals.")

df = st.session_state["dataset"]

if df is not None:
    # Sidebar Filters
    st.sidebar.markdown("### 🎛️ Filter Panel")
    
    # 1. Course Filter
    courses = sorted(list(df["Course"].unique()))
    selected_courses = st.sidebar.multiselect("Courses", courses, default=courses)
    
    # 2. Semester Filter
    semesters = sorted(list(df["Semester"].unique()))
    selected_semesters = st.sidebar.multiselect("Semesters", semesters, default=semesters)
    
    # 3. Gender Filter
    genders = sorted(list(df["Gender"].unique()))
    selected_genders = st.sidebar.multiselect("Gender", genders, default=genders)
    
    # 4. Attendance Slider
    min_att = float(df["Attendance (%)"].min())
    max_att = float(df["Attendance (%)"].max())
    selected_att = st.sidebar.slider(
        "Attendance (%) Range",
        min_value=min_att,
        max_value=max_att,
        value=(min_att, max_att),
        step=1.0
    )
    
    # Filter the dataframe based on sidebar selections
    filtered_df = df[
        (df["Course"].isin(selected_courses)) &
        (df["Semester"].isin(selected_semesters)) &
        (df["Gender"].isin(selected_genders)) &
        (df["Attendance (%)"] >= selected_att[0]) &
        (df["Attendance (%)"] <= selected_att[1])
    ]
    
    if filtered_df.empty:
        st.warning("⚠️ No data matches the current filters. Please adjust the sidebar controls.")
    else:
        st.write(f"📊 Summary statistics calculated across **{len(filtered_df)}** selected student records.")
        
        # Row 1: KPI metrics cards
        subjects = ["Python", "Java", "Dot_Net", "PHP", "MERN"]
        avg_pct = filtered_df["Percentage"].mean()
        best_student = filtered_df.loc[filtered_df["Total"].idxmax()]
        
        # Calculate strongest and weakest subject averages
        sub_averages = filtered_df[subjects].mean().round(2)
        strongest_sub = sub_averages.idxmax()
        strongest_val = sub_averages.max()
        weakest_sub = sub_averages.idxmin()
        weakest_val = sub_averages.min()
        
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
        with col_kpi1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{avg_pct:.2f}%</div>
                    <div class="metric-label">Class Average</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col_kpi2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value" style="font-size:1.8rem; padding: 4px 0;">{strongest_sub}</div>
                    <div class="metric-label">Strongest Subject ({strongest_val})</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col_kpi3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value" style="font-size:1.8rem; padding: 4px 0;">{weakest_sub}</div>
                    <div class="metric-label">Weakest Subject ({weakest_val})</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Row 2: Plots (Subject-wise average and Grade distribution)
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("#### 📘 Subject-wise Performance Averages")
            fig_sub = px.bar(
                x=sub_averages.index,
                y=sub_averages.values,
                text=sub_averages.values,
                labels={"x": "Subjects", "y": "Average Score"},
                color=sub_averages.values,
                color_continuous_scale=px.colors.sequential.Agsunset,
            )
            fig_sub.update_traces(textposition="outside")
            fig_sub.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#d0d0d0", family="Outfit"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.06)", range=[0, 105]),
                xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_sub, use_container_width=True)
            
        with col_chart2:
            st.markdown("#### 🎯 Grade Distribution Share")
            grade_shares = filtered_df["Grade"].value_counts().reset_index()
            grade_shares.columns = ["Grade", "Count"]
            
            fig_grade = px.pie(
                grade_shares,
                values="Count",
                names="Grade",
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_grade.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#d0d0d0", family="Outfit"),
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_grade, use_container_width=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Row 3: Plots (Attendance vs Grade and Course-wise Comparison)
        col_chart3, col_chart4 = st.columns(2)
        
        with col_chart3:
            st.markdown("#### 📈 Attendance vs. Performance Correlation")
            fig_corr = px.scatter(
                filtered_df,
                x="Attendance (%)",
                y="Percentage",
                color="Grade",
                hover_data=["Student_Name", "Course"],
                size="Total",
                color_discrete_sequence=px.colors.qualitative.Vivid
            )
            fig_corr.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#d0d0d0", family="Outfit"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.06)", title="Student Marks Percentage (%)"),
                xaxis=dict(gridcolor="rgba(255,255,255,0.06)", title="Attendance (%)"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_corr, use_container_width=True)
            
        with col_chart4:
            st.markdown("#### 🏫 Course-wise Comparative Performance")
            course_avg = filtered_df.groupby("Course")[subjects].mean().reset_index()
            course_avg_melted = pd.melt(
                course_avg,
                id_vars=["Course"],
                value_vars=subjects,
                var_name="Subject",
                value_name="Average Marks"
            )
            
            fig_course = px.bar(
                course_avg_melted,
                x="Course",
                y="Average Marks",
                color="Subject",
                barmode="group",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_course.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#d0d0d0", family="Outfit"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.06)", range=[0, 105]),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_course, use_container_width=True)
else:
    st.info("No active dataset. Please upload or load a dataset in the Dataset Management page.")
