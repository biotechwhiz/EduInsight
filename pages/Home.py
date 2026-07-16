import streamlit as st
import pandas as pd
import os

# Auto-load demo dataset if nothing loaded
if st.session_state["dataset"] is None:
    demo_path = "data/students.csv"
    if os.path.exists(demo_path):
        try:
            st.session_state["dataset"] = pd.read_csv(demo_path)
            st.session_state["file_name"] = "students.csv (Demo)"
        except Exception as e:
            pass

df = st.session_state["dataset"]

# Renders the Banner and Welcome Title
st.markdown(
    """
    <div class="banner-container">
        <h1 class="banner-title">Welcome to EduInsight</h1>
        <p class="banner-desc">
            A state-of-the-art Student Performance Analytics Dashboard. Transform raw academic datasets into actionable insights. Identify top performers, monitor average marks, flag students needing attention, and analyze grade distributions instantly.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Display the beautiful generated banner image
banner_path = "images/banner.jpg"
if os.path.exists(banner_path):
    st.image(banner_path, width='stretch')

st.markdown("<br>", unsafe_allow_html=True)

# Main section layout
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### 📊 Academic Overview Summary")
    if df is not None:
        # Calculate statistics
        total_students = len(df)
        unique_courses = df["Course"].nunique()
        highest_marks = df["Total"].max()
        highest_pct = df["Percentage"].max()
        avg_percentage = df["Percentage"].mean()
        
        # Pass Percentage (Grade != 'F')
        passed_students = len(df[df["Grade"] != "F"])
        pass_rate = (passed_students / total_students) * 100 if total_students > 0 else 0
        
        # Display KPIs in grid
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        kpi_col4, kpi_col5 = st.columns(2)
        
        with kpi_col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{total_students}</div>
                    <div class="metric-label">Total Students</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with kpi_col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{unique_courses}</div>
                    <div class="metric-label">Active Courses</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with kpi_col3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{highest_marks} <span style="font-size:1.2rem; color:#b0b0b0;">/500</span></div>
                    <div class="metric-label">Highest Total</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with kpi_col4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{avg_percentage:.2f}%</div>
                    <div class="metric-label">Average Percentage</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with kpi_col5:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-value">{pass_rate:.2f}%</div>
                    <div class="metric-label">Overall Pass Rate</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("No dataset is loaded. Please go to Dataset Management to upload a student records file.")

with col_right:
    st.markdown("### 🚀 Quick Navigation")
    st.markdown(
        """
        Explore the modules of the application to interact with your data:
        """
    )
    
    if st.button("📤 Upload New Dataset", width='stretch'):
        st.switch_page("pages/Upload_Dataset.py")
        
    if st.button("👁️ View Full Student Table", width='stretch'):
        st.switch_page("pages/View_Dataset.py")
        
    if st.button("🔍 Search Student Profiles", width='stretch'):
        st.switch_page("pages/Search_Student.py")
        
    if st.button("📈 View Interactive Charts", width='stretch'):
        st.switch_page("pages/Performance_Analysis.py")

st.markdown("<br><hr style='border: 0; height: 1px; background: rgba(255, 255, 255, 0.1);'><br>", unsafe_allow_html=True)

# Add structured features list below
st.markdown("### 🌟 Key Features of EduInsight")
feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown("##### 📁 Seamless Dataset Management")
    st.write("Upload student files in CSV or XLSX format. View dimensions, check column data types, and reload or switch datasets dynamically.")

with feat_col2:
    st.markdown("##### 🔍 Student Lookup Profiles")
    st.write("Find student academic cards by Name or Roll Number. Instantly generate a custom performance radar/bar chart mapping individual grades against class averages.")

with feat_col3:
    st.markdown("##### 📈 Data Science Visualization")
    st.write("Examine subject averages, branch performances, and attendance correlations using interactive Plotly charts with powerful sidebar filtering.")
