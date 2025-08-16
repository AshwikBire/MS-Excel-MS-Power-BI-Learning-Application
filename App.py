# Advanced MS Excel & Power BI Learning App
# Streamlit Version: >=1.22.0

import streamlit as st
import pandas as pd
import plotly.express as px
import webbrowser

st.set_page_config(page_title="Excel & Power BI Learning App", layout="wide")

# --- Custom CSS for multi-colored tabs and vibrant UI ---
st.markdown("""
<style>
/* Tab buttons */
div[data-baseweb="tab"] button {
    background: linear-gradient(90deg, #FF6B6B, #FFD93D);
    color: white;
    font-weight: bold;
    border-radius: 10px 10px 0 0;
}
div[data-baseweb="tab"] button:focus {
    outline: none;
}
.stButton>button {
    background-color: #1E90FF;
    color: white;
    border-radius: 8px;
    padding: 0.5em 1em;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #FF6347;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --- Tab Layout ---
tabs = st.tabs(["🏠 Home", "📚 Quick Links & Learning", "🎥 Recommended Videos", "📝 Practice Material", "📑 Cheat Sheet", "📊 Visuals"])

# -------------------------------
# HOME TAB
# -------------------------------
with tabs[0]:
    st.markdown("<h1 style='color:#FF5733;'>Welcome to Excel & Power BI Learning App</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#2E4053; font-size:18px;'>This app is designed to help you learn Microsoft Excel and Power BI interactively with tutorials, cheat sheets, videos, practice exercises, and visual examples.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("<h2 style='color:#1F618D;'>About Me</h2>", unsafe_allow_html=True)
    st.markdown("""
    **Ashwik Bire**  
    Microsoft Certified Data & Power BI Enthusiast  
    Working to develop interactive learning tools for Excel & Power BI.
    """)
    st.markdown("[LinkedIn Profile](https://www.linkedin.com/in/ashwik-bire/)")

# -------------------------------
# QUICK LINKS & LEARNING MATERIALS TAB
# -------------------------------
with tabs[1]:
    st.markdown("<h1 style='color:#28B463;'>Quick Links & Learning Materials</h1>", unsafe_allow_html=True)
    
    st.markdown("### Excel Important Concepts")
    excel_concepts = [
        "Formulas & Functions", 
        "Pivot Tables & Charts",
        "Conditional Formatting",
        "Data Validation",
        "Lookup Functions (VLOOKUP, HLOOKUP, INDEX, MATCH)",
        "Shortcuts & Tips"
    ]
    for concept in excel_concepts:
        st.markdown(f"- ✅ {concept}")
        
    st.markdown("### Power BI Important Concepts")
    powerbi_concepts = [
        "Data Modeling",
        "DAX Formulas",
        "Visualizations",
        "Power Query / ETL",
        "Reports & Dashboards",
        "Bookmarks & Slicers"
    ]
    for concept in powerbi_concepts:
        st.markdown(f"- ✅ {concept}")
    
    st.markdown("---")
    st.markdown("### Downloadable Resources")
    st.download_button("Download Excel Cheat Sheet", "Excel_Cheat_Sheet.pdf")
    st.download_button("Download Power BI Cheat Sheet", "PowerBI_Cheat_Sheet.pdf")
    
# -------------------------------
# RECOMMENDED VIDEOS TAB
# -------------------------------
with tabs[2]:
    st.markdown("<h1 style='color:#F39C12;'>Recommended Videos</h1>", unsafe_allow_html=True)
    
    st.markdown("### Excel Tutorials")
    excel_videos = {
        "Excel Basics": "https://www.youtube.com/watch?v=rwbho0CgEAE",
        "Excel Formulas Guide": "https://www.youtube.com/watch?v=9NUjHBNWe9M",
        "Pivot Table Tutorial": "https://www.youtube.com/watch?v=9NUjHBNWe9M",
        "Excel Charts Tutorial": "https://www.youtube.com/watch?v=JtM02yW2lVQ"
    }
    for title, link in excel_videos.items():
        st.markdown(f"- [{title}]({link})")
    
    st.markdown("### Power BI Tutorials")
    powerbi_videos = {
        "Power BI Full Course": "https://www.youtube.com/watch?v=AGrl-H87pRU",
        "Power BI DAX Tutorial": "https://www.youtube.com/watch?v=9NUjHBNWe9M",
        "Power BI Data Modeling": "https://www.youtube.com/watch?v=AGrl-H87pRU",
        "Power BI Visuals": "https://www.youtube.com/watch?v=AGrl-H87pRU"
    }
    for title, link in powerbi_videos.items():
        st.markdown(f"- [{title}]({link})")

# -------------------------------
# PRACTICE MATERIAL TAB
# -------------------------------
with tabs[3]:
    st.markdown("<h1 style='color:#AF7AC5;'>Practice Material</h1>", unsafe_allow_html=True)
    
    st.markdown("### Excel MCQs")
    excel_mcq = {
        "Which function sums a range of cells?": ["AVG()", "SUM()", "COUNT()", "MAX()", "SUM()"],
        "Which formula calculates loan payments?": ["FV()", "PMT()", "PV()", "RATE()", "PMT()"]
    }
    for question, options in excel_mcq.items():
        st.markdown(f"**{question}**")
        choice = st.radio("Select answer:", options[:-1], key=question)
        if choice == options[-1]:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Wrong! Correct answer: {options[-1]}")
    
    st.markdown("### Power BI MCQs")
    powerbi_mcq = {
        "Which DAX function returns current year-to-date sum?": ["TOTALYTD()", "SAMEPERIODLASTYEAR()", "SUM()", "CALCULATE()", "TOTALYTD()"],
        "Which function fetches a related table column?": ["RELATED()", "LOOKUPVALUE()", "CALCULATE()", "FILTER()", "RELATED()"]
    }
    for question, options in powerbi_mcq.items():
        st.markdown(f"**{question}**")
        choice = st.radio("Select answer:", options[:-1], key=question+"_pb")
        if choice == options[-1]:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Wrong! Correct answer: {options[-1]}")

# -------------------------------
# CHEAT SHEET TAB
# -------------------------------
with tabs[4]:
    st.markdown("<h1 style='color:#E74C3C;'>Cheat Sheet</h1>", unsafe_allow_html=True)
    
    st.markdown("### Excel Formulas")
    excel_data = {
        "SUM": "SUM(A1:A10) - Adds range of cells",
        "AVERAGE": "AVERAGE(A1:A10) - Average of range",
        "IF": "IF(A1>10,'Yes','No') - Conditional logic",
        "VLOOKUP": "VLOOKUP(10,A1:B10,2,FALSE) - Lookup value",
        "INDEX": "INDEX(A1:B10,2,1) - Return value at row,col",
        "MATCH": "MATCH(10,A1:A10,0) - Return position",
        "TODAY": "TODAY() - Current date",
        "NOW": "NOW() - Current date & time"
    }
    excel_df = pd.DataFrame(excel_data.items(), columns=["Function","Description"])
    st.dataframe(excel_df)
    
    st.markdown("### Power BI DAX Queries")
    powerbi_data = {
        "SUM": "SUM(Sales[Amount]) - Sum of column",
        "AVERAGE": "AVERAGE(Sales[Amount]) - Average of column",
        "CALCULATE": "CALCULATE(SUM(Sales[Amount]), Sales[Region]='West') - Conditional sum",
        "IF": "IF(Sales[Amount]>1000,'High','Low') - Conditional logic",
        "RELATED": "RELATED(Customer[City]) - Fetch related table value",
        "FILTER": "FILTER(Sales, Sales[Amount]>500) - Custom filter",
        "RANKX": "RANKX(ALL(Sales), Sales[Amount]) - Rank values",
        "DATESYTD": "DATESYTD(Sales[Date]) - Year-to-date sum"
    }
    powerbi_df = pd.DataFrame(powerbi_data.items(), columns=["DAX Query","Description"])
    st.dataframe(powerbi_df)

# -------------------------------
# VISUALS TAB
# -------------------------------
with tabs[5]:
    st.markdown("<h1 style='color:#17A589;'>Visualizations</h1>", unsafe_allow_html=True)
    
    st.markdown("### Sample Excel Chart (Column Chart)")
    df_chart = pd.DataFrame({
        "Month": ["Jan","Feb","Mar","Apr","May"],
        "Sales": [2500,3000,2800,3500,4000]
    })
    fig = px.bar(df_chart, x="Month", y="Sales", title="Monthly Sales", color="Sales", color_continuous_scale="Viridis")
    st.plotly_chart(fig)
    
    st.markdown("### Sample Power BI Visual (Simulated KPI)")
    kpi_data = pd.DataFrame({
        "KPI": ["Revenue","Profit","Customers"],
        "Value": [50000,12000,350]
    })
    fig2 = px.bar(kpi_data, x="KPI", y="Value", color="KPI", text="Value", title="Sample KPI Dashboard")
    st.plotly_chart(fig2)
    
    st.markdown("### Interactive Pie Chart Example")
    pie_data = pd.DataFrame({
        "Category":["A","B","C","D"],
        "Values":[20,30,25,25]
    })
    fig3 = px.pie(pie_data, names="Category", values="Values", title="Category Distribution", color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig3)