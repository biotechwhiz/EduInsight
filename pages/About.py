import streamlit as st

st.markdown("## ℹ️ About EduInsight")
st.markdown("Learn more about the project, its core objective, developer information, and technology stack.")

# Two columns layout
col_about, col_tech = st.columns([1.2, 1])

with col_about:
    st.markdown("### 🎯 Project Objective")
    st.write(
        """
        EduInsight is a powerful educational analytics tool designed to process, analyze, and present student performance details.
        
        The primary objective of this application is to help educational institutions:
        - **Automate Academic Analysis:** Instantly analyze records of scores, grades, and attendance without manual math.
        - **Track and Monitor Progress:** Provide interactive visual models highlighting branch-wise, subject-wise, and individual student progress.
        - **Identify Students At-Risk:** Detect performance alerts, low attendance thresholds (< 75%), or failed domains early to plan timely interventions.
        - **Streamline Reporting:** Generate and export detailed data sheets for topper groups, failures, and course summaries.
        """
    )
    
    st.markdown("### 👤 Developer & Project Information")
    st.markdown(
        """
        <div style='background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 18px;'>
            <table style='width:100%; border-collapse:collapse; color:#e0e0e0; font-family:"Outfit",sans-serif; font-size:0.95rem;'>
                <tr style='border-bottom:1px solid rgba(255,255,255,0.05);'><td style='padding:8px 0; font-weight:600; color:#a0a0a0;'>Project Name</td><td style='text-align:right; font-weight:700; color:#ffffff;'>EduInsight - Student Performance Analytics</td></tr>
                <tr style='border-bottom:1px solid rgba(255,255,255,0.05);'><td style='padding:8px 0; font-weight:600; color:#a0a0a0;'>Version</td><td style='text-align:right; font-weight:700; color:#ffffff;'>1.0.0 (Release Build)</td></tr>
                <tr style='border-bottom:1px solid rgba(255,255,255,0.05);'><td style='padding:8px 0; font-weight:600; color:#a0a0a0;'>Lead Developer</td><td style='text-align:right; color:#ffffff;'>Er. Raj Hussain</td></tr>
                <tr style='border-bottom:1px solid rgba(255,255,255,0.05);'><td style='padding:8px 0; font-weight:600; color:#a0a0a0;'>Training Company</td><td style='text-align:right; color:#ffffff;'>Kamadgiri Software Solution (P) Ltd.</td></tr>
                <tr><td style='padding:8px 0; font-weight:600; color:#a0a0a0;'>License</td><td style='text-align:right; color:#2ed573;'>Academic / Open Source</td></tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_tech:
    st.markdown("### 🛠️ Technology Stack")
    st.write("This application is written entirely in **Python** using leading-edge libraries in **AI & Data Science**:")
    
    st.markdown(
        """
        - 🚀 **Streamlit (v1.35.0+):** Modern interactive web application framework.
        - 🐼 **Pandas:** Advanced data structure operations, data cleaning, and CSV/Excel parsing.
        - 📊 **Plotly Express:** Highly customizable and fluid interactive data visualizations.
        - 🔢 **NumPy:** Mathematical computations and vectorization.
        - 📁 **OpenPyXL:** Engine supporting excel document uploads and downloads.
        """
    )
    
    st.markdown("### 🔮 Future Scope")
    st.write(
        """
        Plans to enhance EduInsight include:
        - 🔑 **Authentication & RBAC:** Role-Based Access Control (Admins, Teachers, Students).
        - 🗄️ **Database Integration:** Direct support for Postgres, MySQL, or MongoDB.
        - 📧 **Automated Alerts:** Weekly performance alert newsletters emailed directly to parents or advisors.
        - 🧠 **Predictive AI Modeling:** Machine Learning models forecasting drop-out rates or predicting final scores.
        """
    )
