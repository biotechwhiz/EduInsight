import streamlit as st
import os
import pandas as pd

# Set page config
st.set_page_config(
    page_title="EduInsight - Student Performance Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for global styles
def local_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }
        
        /* Metric cards */
        .metric-card {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-align: center;
            height: 100%;
        }
        .metric-card:hover {
            transform: translateY(-5px);
            border-color: rgba(118, 75, 162, 0.4);
            box-shadow: 0 8px 30px 0 rgba(118, 75, 162, 0.25);
            background: rgba(118, 75, 162, 0.05);
        }
        .metric-value {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }
        .metric-label {
            font-size: 0.85rem;
            color: #b0b0b0;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1.2px;
        }
        
        /* Glowing badges */
        .pass-badge {
            background: rgba(46, 213, 115, 0.15);
            color: #2ed573;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            border: 1px solid rgba(46, 213, 115, 0.3);
            display: inline-block;
        }
        .fail-badge {
            background: rgba(255, 71, 87, 0.15);
            color: #ff4757;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            border: 1px solid rgba(255, 71, 87, 0.3);
            display: inline-block;
        }
        
        /* Modern Header Banner */
        .banner-container {
            background: linear-gradient(135deg, rgba(30, 60, 114, 0.4) 0%, rgba(42, 82, 152, 0.4) 100%);
            border-radius: 20px;
            padding: 35px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }
        
        .banner-title {
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .banner-desc {
            color: #c0c0c0;
            font-size: 1.1rem;
            max-width: 800px;
            line-height: 1.5;
        }
        
        /* Premium custom button style */
        .stButton>button {
            border-radius: 12px !important;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            padding: 12px 28px !important;
            font-weight: 600 !important;
            font-family: 'Outfit', sans-serif !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        }
        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
            border: none !important;
        }
        .stButton>button:active {
            transform: translateY(0px) !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0d0e15 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        
        </style>
    """, unsafe_allow_html=True)

local_css()

# Session State Setup
if "dataset" not in st.session_state:
    st.session_state["dataset"] = None
if "file_name" not in st.session_state:
    st.session_state["file_name"] = None

# Custom Multi-Page Routing
home_page = st.Page("pages/Home.py", title="Home Dashboard", icon="🏠", default=True)
upload_page = st.Page("pages/Upload_Dataset.py", title="Dataset Management", icon="📤")
view_page = st.Page("pages/View_Dataset.py", title="View Dataset", icon="👁️")
search_page = st.Page("pages/Search_Student.py", title="Search Student", icon="🔍")
analysis_page = st.Page("pages/Performance_Analysis.py", title="Performance Analysis", icon="📈")
reports_page = st.Page("pages/Reports.py", title="Performance Reports", icon="📋")
about_page = st.Page("pages/About.py", title="About EduInsight", icon="ℹ️")

# Initialize navigation
pg = st.navigation({
    "EduInsight Menu": [
        home_page, 
        upload_page, 
        view_page, 
        search_page, 
        analysis_page, 
        reports_page, 
        about_page
    ]
})

# Sidebar Logo and Branding
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        logo_path = "images/logo.jpg"
        if os.path.exists(logo_path):
            st.image(logo_path, width=90)
    
    st.markdown(
        """
        <div style='text-align: center;'>
            <h2 style='margin-top: 5px; margin-bottom: 0px; font-weight: 800; font-family: "Outfit", sans-serif; background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>EduInsight</h2>
            <p style='color: #8a8d9a; font-size: 0.85rem; font-weight: 500; letter-spacing: 0.5px; margin-bottom: 20px;'>Student Performance Analytics</p>
        </div>
        <hr style='border: 0; height: 1px; background: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(255, 255, 255, 0.08), rgba(0, 0, 0, 0)); margin-bottom: 15px;'>
        """,
        unsafe_allow_html=True
    )

# Run the selected page
pg.run()

# Sidebar Footer
with st.sidebar:
    st.markdown(
        """
        <hr style='border: 0; height: 1px; background: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(255, 255, 255, 0.08), rgba(0, 0, 0, 0)); margin-top: 20px; margin-bottom: 15px;'>
        <div style='text-align: center; color: #5f616e; font-size: 0.8rem; font-family: "Outfit", sans-serif;'>
            EduInsight v1.0.0<br>
            Developed by: Er. Raj Hussain
        </div>
        """,
        unsafe_allow_html=True
    )
