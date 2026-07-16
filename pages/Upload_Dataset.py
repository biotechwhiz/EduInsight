import streamlit as st
import pandas as pd
import os

st.markdown("## 📤 Dataset Management")
st.markdown("Upload student records in CSV or Excel format to begin analyzing academic performance, or use the pre-configured demo dataset.")

# File uploader widget
uploaded_file = st.file_uploader("Upload student CSV/Excel dataset", type=["csv", "xlsx"])

col_action1, col_action2, _ = st.columns([1, 1, 2])

with col_action1:
    if st.button("🔄 Load Demo Dataset", width='stretch'):
        demo_path = "data/students.csv"
        if os.path.exists(demo_path):
            try:
                st.session_state["dataset"] = pd.read_csv(demo_path)
                st.session_state["file_name"] = "students.csv (Demo)"
                st.success("Demo dataset loaded successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading demo dataset: {e}")
        else:
            st.error("Demo dataset file not found at data/students.csv")

with col_action2:
    if st.button("🗑️ Clear Dataset", width='stretch'):
        st.session_state["dataset"] = None
        st.session_state["file_name"] = None
        st.info("Active dataset cleared.")
        st.rerun()

# Processing the uploaded file
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        # Standard validation of critical fields
        critical_cols = ["Roll_No", "Student_Name"]
        missing_crit = [col for col in critical_cols if col not in df.columns]
        
        if missing_crit:
            st.error(f"Failed to load: Uploaded dataset must contain at least the following columns: {', '.join(missing_crit)}")
        else:
            # Check for other columns and calculate totals/averages if missing
            subject_cols = ["Python", "Java", "Dot_Net", "PHP", "MERN"]
            missing_subjects = [col for col in subject_cols if col not in df.columns]
            
            # Recalculate columns if marks are present but Total/Percentage/Grade are not
            present_subjects = [col for col in subject_cols if col in df.columns]
            
            if "Total" not in df.columns and len(present_subjects) > 0:
                df["Total"] = df[present_subjects].sum(axis=1)
                
            if "Percentage" not in df.columns and "Total" in df.columns:
                df["Percentage"] = (df["Total"] / (len(present_subjects) * 100)) * 100
                df["Percentage"] = df["Percentage"].round(2)
                
            if "Grade" not in df.columns and "Percentage" in df.columns:
                grades = []
                for p in df["Percentage"]:
                    if p >= 90: grades.append("A+")
                    elif p >= 80: grades.append("A")
                    elif p >= 70: grades.append("B")
                    elif p >= 60: grades.append("C")
                    elif p >= 50: grades.append("D")
                    else: grades.append("F")
                df["Grade"] = grades
                
            st.session_state["dataset"] = df
            st.session_state["file_name"] = uploaded_file.name
            st.success(f"Dataset '{uploaded_file.name}' uploaded and processed successfully!")
            st.rerun()
            
    except Exception as e:
        st.error(f"Error parsing file: {e}")

# Display details of loaded dataset
df = st.session_state["dataset"]
if df is not None:
    st.markdown("---")
    st.markdown(f"### 📋 Loaded Dataset Information: `{st.session_state['file_name']}`")
    
    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.metric("Total Records (Rows)", f"{len(df)}")
    with info_col2:
        st.metric("Total Variables (Columns)", f"{len(df.columns)}")
    with info_col3:
        file_ext = "CSV" if ".csv" in st.session_state["file_name"].lower() else "Excel (.xlsx)"
        st.metric("File Format", file_ext)
        
    st.markdown("#### 🔍 Dataset Preview (First 5 Rows)")
    st.dataframe(df.head(5), width='stretch')
    
    st.markdown("#### 📂 Schema Details")
    schema_df = pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": [str(x) for x in df.dtypes],
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values
    })
    st.dataframe(schema_df, width='stretch', hide_index=True)
else:
    st.info("No active dataset. Upload a CSV/Excel file or load the demo dataset above.")
