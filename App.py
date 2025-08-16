import streamlit as st

# --------- PAGE CONFIGURATION ----------
st.set_page_config(
    page_title="Data Analytics Learning Hub",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# --------- CUSTOM CSS FOR DARK THEME AND ACCENTS ----------
st.markdown(
    """
    <style>
    /* General background and text colors */
    .main{
        background-color: #121212;
        color: #E0E0E0;
    }
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #000000;
        color: #E0E0E0;
    }
    /* Sidebar headings */
    [data-testid="stSidebar"] h2 {
        color: #0099FF;
    }
    /* Tabs styled as buttons */
    .tab-button {
        background-color: #000000;
        border: 2px solid #0099FF;
        color: #0099FF;
        padding: 10px 30px;
        margin: 5px 10px 15px 0;
        border-radius: 12px;
        cursor: pointer;
        font-weight: 600;
        font-size: 16px;
        display: inline-block;
        transition: all 0.3s ease;
    }
    .tab-button:hover {
        background-color: #0099FF;
        color: #121212;
        border: 2px solid #FF3333;
    }
    .tab-button.selected {
        background-color: #FF3333;
        color: #121212;
        border: 2px solid #FF3333;
    }
    /* Headers */
    h1, h2, h3, h4, h5 {
        color: #0099FF;
    }
    /* Links */
    a {
        color: #FF3333;
        text-decoration: none;
        font-weight: 600;
    }
    a:hover {
        text-decoration: underline;
    }
    /* Buttons */
    button {
        background-color: #0099FF !important;
        color: #121212 !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
    }
    /* Download button */
    button[title="download file"] {
        background-color: #FF3333 !important;
        color: #121212 !important;
    }
    /* Footer with subtle color */
    footer {
        color: #888888;
        font-size: 12px;
        margin-top: 30px;
    }
    /* Video embed borders */
    iframe {
        border-radius: 15px;
        border: 3px solid #0099FF;
    }

    </style>
    """, unsafe_allow_html=True)

# --------- APP TITLE AND INTRO ----------
st.title("📊 Data Analytics Learning Hub")
st.markdown(
    """
    Welcome to this comprehensive learning app focused on **MS Power BI** and **Excel** for aspiring data professionals.
    This platform contains rich learning materials, quick access to resources, practice exercises, and curated video tutorials.

    ---  
    Developed by [Your Name](https://linkedin.com/in/yourprofile) — Junior Data Scientist | Python & Streamlit Enthusiast  
    """
)

# --------- TAB NAVIGATION BUTTONS ----------
tabs = [
    "Home",
    "Quick Links & Materials",
    "Power BI Concepts",
    "Excel Concepts",
    "Practice Materials",
    "Recommended Videos"
]

# Initialize session state for tab selection
if "tab_selected" not in st.session_state:
    st.session_state.tab_selected = "Home"

def set_tab(tab_name):
    st.session_state.tab_selected = tab_name

# Buttons for tabs with styling
tab_cols = st.container()
with tab_cols:
    col1, col2, col3, col4, col5, col6 = st.columns(len(tabs))
    buttons = [col1, col2, col3, col4, col5, col6]
    for idx, tab in enumerate(tabs):
        selected = st.session_state.tab_selected == tab
        btn_style = "tab-button selected" if selected else "tab-button"
        if buttons[idx].button(tab, key=tab, help=f"Go to {tab} tab"):
            set_tab(tab)
            st.experimental_rerun()

# --------- TAB CONTENTS -----------

# HOME TAB - Introduction
if st.session_state.tab_selected == "Home":
    st.header("Welcome!")
    st.markdown(
        """
        This application is designed to be your **go-to platform** for learning and mastering Power BI and Excel.
        
        **Features:**
        - Easy-to-navigate color-coded tabs
        - Curated quick learning links and practice files
        - In-depth concepts breakdown for Power BI and Excel
        - Embedded video tutorials for practical learning
        - Interactive quizzes and downloadable resources
        
        Navigate through the tabs above to explore content.
        """
    )
    st.image(
        "https://images.unsplash.com/photo-1531497865144-9a4a41fbbc45?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        caption="Learn Data Analytics with Power BI & Excel",
        use_column_width=True
    )

# QUICK LINKS TAB
elif st.session_state.tab_selected == "Quick Links & Materials":
    st.header("Quick Links & Learning Materials")
    st.markdown(
        """
        Find here essential external resources carefully curated to improve your skills.
        """
    )
    st.markdown(
        """
        - [Power BI Full Course for Beginners - YouTube](https://www.youtube.com/watch?v=FwjaHCVNBWA)
        - [Excel to Power BI Transition - Coursera](https://www.coursera.org/learn/from-excel-to-power-bi)
        - [Microsoft Power BI Documentation](https://docs.microsoft.com/en-us/power-bi/)
        - [Excel Official Tutorials](https://support.microsoft.com/en-us/excel)
        """
    )
    st.markdown("### Downloads")
    st.download_button("Download Power BI Cheat Sheet (PDF)", data="Power BI Cheat Sheet Content Placeholder", file_name="powerbi_cheatsheet.pdf")
    st.download_button("Download Excel Formulas Guide (PDF)", data="Excel Formulas Guide Content Placeholder", file_name="excel_formulas_guide.pdf")

# POWER BI CONCEPTS TAB
elif st.session_state.tab_selected == "Power BI Concepts":
    st.header("Power BI Concepts")
    st.markdown("""
    Gain mastery over critical Power BI components:
    - **Data Modeling & Relationships**
    - **DAX - Data Analysis Expressions**
    - **Power Query & Data Transformation**
    - **Report & Dashboard Development**
    - **Power BI Service & Sharing**
    """)
    with st.expander("Detailed Overview: Data Modeling & Relationships"):
        st.write("Understand how tables relate, setting cardinality, and relationship types.")
    with st.expander("Detailed Overview: DAX"):
        st.write("Learn calculated columns, measures, variables, and time intelligence.")
    with st.expander("Detailed Overview: Reports & Dashboards"):
        st.write("Building interactive visuals, filters, slicers, and layouts.")
    with st.expander("Data Sources & Power Query"):
        st.write("Data import types, cleaning, and preparation.")

# EXCEL CONCEPTS TAB
elif st.session_state.tab_selected == "Excel Concepts":
    st.header("Excel Important Concepts")
    st.markdown("""
    Key topics for Excel proficiency:
    - **Formulas and Functions (VLOOKUP, XLOOKUP, IF, SUMIF)**
    - **Pivot Tables and Pivot Charts**
    - **Conditional Formatting & Data Validation**
    - **Excel Tables & Named Ranges**
    - **Charts & Dashboarding**
    """)
    with st.expander("Formulas and Functions"):
        st.write("Deep dive into lookup functions, logical tests, and aggregation functions.")
    with st.expander("Pivot Tables & Charts"):
        st.write("Summarizing data, grouping, and dynamic charting.")
    with st.expander("Dashboarding Tips"):
        st.write("Interactive Excel dashboards using slicers and dynamic ranges.")

# PRACTICE MATERIALS TAB
elif st.session_state.tab_selected == "Practice Materials":
    st.header("Practice Material and Exercises")
    st.markdown("Develop your skills by practicing with these downloadable files and quizzes:")
    st.download_button(
        label="Download Excel Practice File",
        data="Excel practice file data placeholder",
        file_name="excel_practice.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.download_button(
        label="Download Power BI Dataset",
        data="Power BI dataset file content placeholder",
        file_name="powerbi_data.csv",
        mime="text/csv"
    )
    st.markdown("#### Practice Quiz")
    quiz_q1 = st.radio("What does DAX stand for in Power BI?", ["Data Analysis Expressions", "Dynamic Analysis X", "Digital Analytics X"], key="quiz1")
    quiz_q2 = st.radio("Which Excel function helps to look up values in a table?", ["VLOOKUP", "SUMIF", "CONCATENATE"], key="quiz2")
    if st.button("Submit Quiz"):
        score = 0
        if quiz_q1 == "Data Analysis Expressions":
            score += 1
        if quiz_q2 == "VLOOKUP":
            score += 1
        st.success(f"Your score: {score}/2")

# RECOMMENDED VIDEOS TAB
elif st.session_state.tab_selected == "Recommended Videos":
    st.header("Recommended Learning Videos")
    st.markdown("Embedded videos for deep learning and concept clarity.")
    st.video("https://www.youtube.com/watch?v=FwjaHCVNBWA")  # Power BI full course
    st.video("https://www.youtube.com/watch?v=dX9Ihyns5dA")  # Excel basics tutorial
    st.video("https://www.youtube.com/watch?v=vxCxhD7Q0Po")  # Advanced Power BI features

# --------- FOOTER ----------
st.markdown(
    """
    <footer>
    &copy; 2025 Data Analytics Learning Hub | Built with Streamlit & ❤️
    </footer>
    """, unsafe_allow_html=True
)
