import streamlit as st
import pandas as pd

st.markdown("## 👁️ View Dataset")
st.markdown("Browse, filter, and inspect the entire student dataset. You can sort rows by clicking on headers.")

df = st.session_state["dataset"]

if df is not None:
    # Summary of size
    rows, cols = df.shape
    
    metric_col1, metric_col2, metric_col3 = st.columns([1, 1, 2])
    with metric_col1:
        st.metric("Total Records (Rows)", f"{rows}")
    with metric_col2:
        st.metric("Attributes (Columns)", f"{cols}")
        
    st.markdown("---")
    
    # Advanced inline search and filtering options
    st.markdown("#### 🔍 Search & Quick Filters")
    f_col1, f_col2, f_col3 = st.columns(3)
    
    with f_col1:
        search_query = st.text_input("Search student name or roll number", value="")
    with f_col2:
        # Dynamic course selector
        available_courses = ["All"] + sorted(list(df["Course"].unique()))
        selected_course = st.selectbox("Filter by Course", available_courses)
    with f_col3:
        # Dynamic grade selector
        available_grades = ["All"] + sorted(list(df["Grade"].unique()))
        selected_grade = st.selectbox("Filter by Grade", available_grades)
        
    # Apply filters
    filtered_df = df.copy()
    
    if search_query:
        filtered_df = filtered_df[
            filtered_df["Student_Name"].str.contains(search_query, case=False, na=False) |
            filtered_df["Roll_No"].astype(str).str.contains(search_query, na=False)
        ]
        
    if selected_course != "All":
        filtered_df = filtered_df[filtered_df["Course"] == selected_course]
        
    if selected_grade != "All":
        filtered_df = filtered_df[filtered_df["Grade"] == selected_grade]
        
    # Row matching indicator
    if len(filtered_df) < rows:
        st.caption(f"Showing {len(filtered_df)} records matching the selected filters out of {rows} total.")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display dataframe
    st.dataframe(filtered_df, width='stretch', hide_index=True)
    
    # Download and refresh buttons
    b_col1, b_col2, _ = st.columns([1, 1.2, 2.8])
    
    with b_col1:
        if st.button("🔄 Refresh Table", width='stretch'):
            st.rerun()
            
    with b_col2:
        # Export option
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Table as CSV",
            data=csv,
            file_name="student_records.csv",
            mime="text/csv",
            width='stretch'
        )
else:
    st.info("No active dataset. Please upload or load a dataset in the Dataset Management page.")
