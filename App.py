# Learning_Dark_UI_App_With_LinkedIn_YouTube.py
# Excel & Power BI Learning Hub - Dark Themed Streamlit App
# UTF-8 safe (no emoji). Includes LinkedIn link for Ashwik and YouTube recommendations on Home.
# Requires: streamlit, pandas, numpy, plotly, altair, openpyxl
# Run: streamlit run Learning_Dark_UI_App_With_LinkedIn_YouTube.py

import streamlit as st
import pandas as pd
import numpy as np
import io
import base64
import sqlite3
import plotly.express as px
import altair as alt
from datetime import datetime

# ---------------- App config ----------------
st.set_page_config(
    page_title="Excel & Power BI Learning Hub (Dark)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Dark CSS ----------------
def inject_dark_css():
    css = """
    <style>
    :root {
        --bg: #0b1220;
        --card: #0f1720;
        --muted: #9ca3af;
        --accent: #06b6d4;
        --accent-2: #7c3aed;
        --text: #e6eef8;
        --secondary: #cbd5e1;
        --border: rgba(255,255,255,0.06);
    }
    .stApp {
        background: linear-gradient(180deg, var(--bg) 0%, #06111a 100%);
        color: var(--text);
        font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }
    .big-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-radius: 12px;
        padding: 16px;
        border: 1px solid var(--border);
        box-shadow: 0 6px 18px rgba(2,6,23,0.6);
    }
    .muted { color: var(--muted); font-size: 0.95rem; }
    .download-link {
        background: rgba(124,58,237,0.12);
        padding: 6px 10px;
        border-radius: 8px;
        color: var(--accent-2);
        text-decoration: none;
    }
    .progress-badge {
        background: rgba(6,182,212,0.10);
        padding: 6px 10px;
        border-radius: 999px;
        color: var(--accent);
        font-weight: 600;
    }
    .small-note { color: var(--secondary); font-size:0.95rem; }
    .section-title { color: var(--text); font-weight:700; }
    .stDataFrame table { color: var(--text); }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

inject_dark_css()

# ---------------- Utilities ----------------
def sample_data(rows: int = 400, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today(), periods=rows)
    df = pd.DataFrame({
        "Date": rng.choice(dates, size=rows),
        "Region": rng.choice(["North", "South", "East", "West"], size=rows),
        "Product": rng.choice(["Alpha", "Beta", "Gamma", "Delta", "Epsilon"], size=rows),
        "Channel": rng.choice(["Retail", "Online", "Wholesale"], size=rows, p=[0.5,0.35,0.15]),
        "Units": rng.integers(1, 120, size=rows),
        "Price": np.round(rng.uniform(20, 1500, size=rows), 2)
    })
    df["Revenue"] = (df["Units"] * df["Price"]).round(2)
    df["MarginPercent"] = np.round(rng.uniform(5, 35, size=rows), 2)
    df["MarginValue"] = np.round(df["Revenue"] * df["MarginPercent"] / 100, 2)
    return df.sort_values("Date").reset_index(drop=True)

def to_excel_bytes(df: pd.DataFrame, sheet_name: str = "Sheet1") -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        try:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
        except Exception:
            df2 = df.copy()
            for c in df2.columns:
                if df2[c].dtype == "object":
                    df2[c] = df2[c].astype(str)
            df2.to_excel(writer, index=False, sheet_name=sheet_name)
    return output.getvalue()

def excel_download_link(df: pd.DataFrame, filename: str = "data.xlsx", label: str = "Download Excel"):
    b = to_excel_bytes(df)
    b64 = base64.b64encode(b).decode()
    href = f"data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}"
    st.markdown(f'<a class="download-link" href="{href}" download="{filename}">{label}</a>', unsafe_allow_html=True)

# ---------------- DB progress ----------------
DB_PATH = "learning_progress.db"
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    init_db(conn)
    return conn

def init_db(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            created_at TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            section TEXT,
            subtopic TEXT,
            status TEXT,
            score INTEGER,
            updated_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            content TEXT,
            created_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()

conn = get_conn()

def ensure_user(conn, name: str) -> int:
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE name = ?", (name,))
    r = cur.fetchone()
    if r:
        return r[0]
    cur.execute("INSERT INTO users (name, created_at) VALUES (?, ?)", (name, datetime.utcnow().isoformat()))
    conn.commit()
    return cur.lastrowid

def save_progress(user_id: int, section: str, subtopic: str, status: str = "incomplete", score: int = -1):
    cur = conn.cursor()
    cur.execute("INSERT INTO progress (user_id, section, subtopic, status, score, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, section, subtopic, status, score, datetime.utcnow().isoformat()))
    conn.commit()

def user_progress_summary(user_id: int) -> pd.DataFrame:
    cur = conn.cursor()
    cur.execute("SELECT section, subtopic, status, score, updated_at FROM progress WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    if not rows:
        return pd.DataFrame(columns=["section", "subtopic", "status", "score", "updated_at"])
    df = pd.DataFrame(rows, columns=["section", "subtopic", "status", "score", "updated_at"])
    return df

# ---------------- Sidebar / Navigation ----------------
st.sidebar.markdown("<div class='big-card'>", unsafe_allow_html=True)
st.sidebar.title("Navigation & Profile")
st.sidebar.write("Jump to learning modules and quick resources.")

if "user_name" not in st.session_state:
    st.session_state.user_name = "Guest"

st.session_state.user_name = st.sidebar.text_input("Your name", value=st.session_state.user_name)
USER_ID = ensure_user(conn, st.session_state.user_name)

# LinkedIn link (user provided)
LINKEDIN_URL = "https://www.linkedin.com/in/ashwik-bire-b2a000186"
st.sidebar.markdown(f"**Connect:** [LinkedIn]({LINKEDIN_URL})")

# Learning navigation with subtopics
learning_nav = {
    "Home": ["Overview", "Roadmap", "YouTube Recommendations"],
    "Dataset Explorer": ["Upload & Inspect", "Cleaning Tools", "Quick Exports"],
    "Excel Basics": ["Introduction", "Formatting & Shortcuts", "Basic Formulas", "Simple Charts"],
    "Excel Advanced": ["Lookup & Reference", "Advanced Formulas", "PivotTables", "Data Validation & Conditional Formatting"],
    "Power BI Basics": ["Interface & Concepts", "Importing Data", "Basic Visuals", "Slicers & Filters"],
    "Power BI Advanced": ["Data Modeling", "Relationships", "DAX Intro", "Performance Tips"],
    "Power Query": ["Transforms (M) concepts", "Unpivot/Pivot", "Merging & Appending"],
    "Visualizations": ["Plotly Examples", "Altair Examples", "Storytelling & Design"],
    "Practice & Quizzes": ["Exercises", "Mini Quizzes", "Auto-check"],
    "Templates & Cheatsheets": ["Excel Templates", "Power BI Templates", "Cheatsheets"],
    "Profile & Progress": ["Saved Notes", "Progress History"],
    "Resources & Export": ["External Links", "Export Study Pack"]
}

page = st.sidebar.selectbox("Select Module", list(learning_nav.keys()), index=0)
st.sidebar.markdown("---")
st.sidebar.markdown("Quick links:")
st.sidebar.markdown("- [Official Excel docs](https://support.microsoft.com/excel)")
st.sidebar.markdown("- [Power BI Learning](https://learn.microsoft.com/power-bi/)")
st.sidebar.markdown(f"- [My LinkedIn]({LINKEDIN_URL})")
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown("<div class='big-card'>", unsafe_allow_html=True)
hcol1, hcol2 = st.columns([3, 1])
with hcol1:
    st.title("Excel & Power BI Learning Hub")
    st.markdown("Hands-on lessons, practical exercises, and downloadable templates. Dark theme for comfortable long sessions.")
with hcol2:
    st.markdown(f"<div style='text-align:right'><div class='progress-badge'>User: {st.session_state.user_name}</div></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Global sample data ----------------
if "sample_df" not in st.session_state:
    st.session_state.sample_df = sample_data(400)

# ---------- Page Implementations ----------
def page_home():
    st.header("Welcome — About this App")
    st.markdown("""
    **Introduction:**  
    Welcome to the *Excel & Power BI Learning Hub* — a focused, hands-on learning workspace designed to take you from Excel basics to Power BI report-building and data modeling.  
    The app is organized as modules (left navigation). Each module contains:
    - Explanations & short theory notes  
    - Interactive demos (using sample data)  
    - Downloadable templates & solutions  
    - Practice exercises that save progress locally
    """)
    st.markdown("**How to use this app effectively:**")
    st.markdown("""
    1. Start with **Excel Basics** then move to **Excel Advanced**.  
    2. Use **Dataset Explorer** to import and clean your own files.  
    3. Practice each exercise in **Practice & Quizzes** and save notes under **Profile & Progress**.  
    4. Explore **Power Query** and **Power BI** modules when you're comfortable with Excel transformations and pivoting.
    """)
    st.markdown("---")
    st.subheader("Quick start — sample dataset preview")
    df = st.session_state.sample_df.copy()
    st.dataframe(df.head(120))
    agg = df.groupby("Region").agg(TotalRevenue=("Revenue", "sum")).reset_index()
    fig = px.bar(agg, x="Region", y="TotalRevenue", title="Sample: Revenue by Region", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("YouTube Recommendations — Channels & Playlists")
    st.markdown("Below are highly-regarded YouTube channels and playlists that pair well with the lessons in this app. These are great for video-based walkthroughs and additional practice.")
    st.markdown("""
    - **Leila Gharani (Excel deep dives & practical use-cases)** — https://www.youtube.com/@LeilaGharani  
    - **ExcelIsFun (Huge library of Excel examples & formulas)** — https://www.youtube.com/user/ExcelIsFun  
    - **MyOnlineTrainingHub (Excel tutorials & dashboards)** — https://www.youtube.com/@MyOnlineTrainingHub  
    - **Guy in a Cube (Power BI tutorials, DAX & reporting tips)** — https://www.youtube.com/@GuyinaCube  
    - **Curbal (Power BI & DAX practical tutorials)** — https://www.youtube.com/@Curbal
    """)
    st.markdown("Tip: follow a lesson here and watch 1-2 short videos from the relevant channel (10–20 minutes) to reinforce the concept.")

    st.markdown("---")
    st.subheader("Suggested learning path (4 weeks)")
    st.markdown("""
    - **Week 1:** Excel Basics — import, formats, basic formulas, simple charts.  
    - **Week 2:** PivotTables, Lookup functions, conditional formatting.  
    - **Week 3:** Power Query transforms, data modeling & relationships.  
    - **Week 4:** DAX basics, measures, visualization design & storytelling.
    """)

def page_dataset_explorer():
    st.header("Dataset Explorer")
    st.markdown("Upload your file or use the sample dataset to inspect structure, dtypes and basic cleaning options.")
    uploaded = st.file_uploader("Upload CSV / Excel file", type=["csv", "xlsx", "xls"])
    if uploaded:
        try:
            if uploaded.name.lower().endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            st.session_state.sample_df = df.copy()
            st.success(f"Loaded {uploaded.name} ({df.shape[0]} rows, {df.shape[1]} cols)")
        except Exception as e:
            st.error("Failed to read file: " + str(e))
            df = st.session_state.sample_df.copy()
    else:
        st.info("No file uploaded — using sample dataset.")
        df = st.session_state.sample_df.copy()

    with st.expander("Data preview (first 500 rows)"):
        st.dataframe(df.head(500))

    with st.expander("Column types & summary"):
        st.write("Shape:", df.shape)
        dtypes = pd.DataFrame({"column": df.columns, "dtype": [str(df[c].dtype) for c in df.columns]})
        st.table(dtypes)

    with st.expander("Cleaning tools"):
        cols = df.columns.tolist()
        to_drop = st.multiselect("Columns to drop", cols)
        if st.button("Drop selected columns"):
            if to_drop:
                df = df.drop(columns=to_drop)
                st.session_state.sample_df = df
                st.success(f"Dropped columns: {', '.join(to_drop)}")
                st.dataframe(df.head(50))
            else:
                st.info("No columns selected.")
        numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        if numeric_cols:
            fill_choice = st.selectbox("Fill missing numeric values with", ["Do nothing", "0", "mean", "median"])
            if st.button("Apply numeric fill"):
                if fill_choice == "0":
                    df[numeric_cols] = df[numeric_cols].fillna(0)
                elif fill_choice == "mean":
                    for c in numeric_cols:
                        df[c] = df[c].fillna(df[c].mean())
                elif fill_choice == "median":
                    for c in numeric_cols:
                        df[c] = df[c].fillna(df[c].median())
                st.session_state.sample_df = df
                st.success("Applied fill to numeric columns.")
                st.dataframe(df.head(50))

    st.markdown("### Quick exports")
    excel_download_link(df.head(200), filename="explorer_export.xlsx", label="Download preview as Excel")

def page_excel_basics():
    st.header("Excel Basics")
    st.markdown("Fundamentals: workbook, worksheet, cells, formulas and basic charts")
    st.subheader("Topics covered")
    st.markdown("""
    - Excel interface & shortcuts  
    - Data types and formatting (dates, numbers, text)  
    - Basic formulas: SUM, AVERAGE, MIN, MAX, COUNT, COUNTA  
    - Relative vs absolute references ($A$1)  
    - Simple charts: column, line, pie
    """)
    st.subheader("Interactive demos (Pandas based)")
    df = st.session_state.sample_df.copy()
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
    st.markdown("**Preview sample dataset**")
    st.dataframe(df.head(200))

    st.markdown("**Formatting examples**")
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        if st.button("Show first 10 rows"):
            st.dataframe(df.head(10))
    with fcol2:
        if st.button("Show descriptive stats"):
            st.dataframe(df.describe(include="all").T)

    st.markdown("**Basic formulas (pandas equivalents)**")
    if st.button("Add 'RevenuePerUnit' column (Price/Units)"):
        df["RevenuePerUnit"] = np.round(df["Revenue"] / df["Units"].replace({0:np.nan}), 2)
        st.session_state.sample_df = df
        st.dataframe(df[["Units", "Price", "RevenuePerUnit"]].head(10))

    st.markdown("**Simple chart: Revenue by Product**")
    agg = df.groupby("Product")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=False)
    fig = px.bar(agg, x="Product", y="Revenue", title="Revenue by Product (sample)", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Excel tips**")
    st.markdown("""
    - Use Freeze Panes to keep headers visible.  
    - Use Format Painter to copy cell formatting.  
    - Use keyboard shortcuts: Ctrl+C, Ctrl+V, Ctrl+Z, Ctrl+Shift+L (filters).
    """)

def page_excel_advanced():
    st.header("Excel Advanced")
    st.markdown("Lookup formulas, PivotTables, Data validation, conditional formatting and advanced charts")
    st.subheader("Lookup & reference")
    df = st.session_state.sample_df.copy()
    lookup = pd.DataFrame({
        "Product": ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"],
        "Category": ["Core", "Core", "Extended", "Extended", "Special"],
        "LaunchYear": [2018, 2019, 2020, 2021, 2022]
    })
    st.markdown("**Lookup table (example)**")
    st.dataframe(lookup)

    st.markdown("**INDEX / MATCH (pandas equivalent: merge)**")
    merged = df.merge(lookup, on="Product", how="left")
    st.dataframe(merged[["Product", "Category", "LaunchYear"]].drop_duplicates().head(10))

    st.subheader("PivotTables")
    st.markdown("Create pivot-like aggregations using pandas pivot_table.")
    cols = df.columns.tolist()
    index = st.multiselect("Pivot index (rows)", cols, default=["Region"])
    columns_choice = st.multiselect("Pivot columns", cols, default=["Product"])
    values = st.selectbox("Pivot values (numeric)", [c for c in cols if pd.api.types.is_numeric_dtype(df[c])], index=cols.index("Revenue") if "Revenue" in cols else 0)
    agg = st.selectbox("Aggregation function", ["sum", "mean", "count", "median", "min", "max"], index=0)
    if st.button("Generate pivot (Advanced)"):
        try:
            pivot = pd.pivot_table(df, index=index or None, columns=columns_choice or None, values=values, aggfunc=agg, margins=True, fill_value=0)
            st.dataframe(pivot)
            st.download_button("Download pivot (Advanced)", data=to_excel_bytes(pivot.reset_index()), file_name="pivot_advanced.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            save_progress(USER_ID, "Excel Advanced", "Pivot created", status="complete", score=95)
        except Exception as e:
            st.error("Pivot creation failed: " + str(e))

    st.subheader("Data validation & Conditional Formatting (concepts)")
    st.markdown("""
    - Data Validation: restrict cell inputs to lists, dates, numbers.  
    - Conditional Formatting: highlight top/bottom, use color scales, use custom formulas.
    """)

def page_power_bi_basics():
    st.header("Power BI Basics")
    st.markdown("Power BI Desktop overview, importing data, creating visuals, and publishing concepts.")
    st.markdown("""
    **Key concepts**  
    - Reports: pages with visuals built from model data  
    - Datasets: tables imported into the model  
    - Dashboards (Power BI Service): pin visuals for single-pane insights  
    - Slicers & interactions: enable users to filter visuals
    """)
    st.subheader("Demo: Import & create visuals (simulated using sample data)")
    df = st.session_state.sample_df.copy()
    st.dataframe(df.head(150))

    st.markdown("**Basic visuals example**")
    fig = px.pie(df.groupby("Channel")["Revenue"].sum().reset_index(), names="Channel", values="Revenue", title="Revenue by Channel", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Publishing & sharing**")
    st.markdown("""
    - Use Power BI Service to publish reports from Desktop.  
    - Set scheduled refresh for cloud datasets.  
    - Use workspace permissions to share with team members.
    """)

def page_power_bi_advanced():
    st.header("Power BI Advanced")
    st.markdown("Data modeling, relationships, DAX measures, and performance optimization.")
    st.subheader("Modeling: star schema")
    df = st.session_state.sample_df.copy()
    dim_product = df[["Product"]].drop_duplicates().reset_index(drop=True)
    dim_region = df[["Region"]].drop_duplicates().reset_index(drop=True)
    fact = df[["Date", "Product", "Region", "Units", "Price", "Revenue"]]
    st.markdown("Example: Fact table (sample)")
    st.dataframe(fact.head(10))
    st.markdown("Example: Dimension tables")
    st.dataframe(dim_product.head(10))
    st.dataframe(dim_region.head(10))

    st.subheader("DAX basics (conceptual & pandas analogues)")
    st.markdown("""
    - Measures (calculations evaluated at query time)  
    - Calculated columns (persisted per row)  
    - Time intelligence: YTD, MTD, QoQ growth
    """)
    if st.button("Show Measure examples (pandas)"):
        measures = {
            "TotalRevenue": round(df["Revenue"].sum(), 2),
            "AvgPrice": round(df["Price"].mean(), 2),
            "DistinctProducts": int(df["Product"].nunique())
        }
        st.table(pd.DataFrame.from_dict(measures, orient="index", columns=["Value"]))

    st.subheader("Performance tips")
    st.markdown("""
    - Import only needed columns and rows.  
    - Use proper data types (integers, datetime).  
    - Reduce cardinality in dimension columns where possible.  
    - Prefer measures over calculated columns for aggregated logic.
    """)

def page_power_query():
    st.header("Power Query (Transformations)")
    st.markdown("Common ETL-like transformations using pandas to emulate Power Query actions.")
    df = st.session_state.sample_df.copy()
    st.markdown("**Unpivot / Pivot example**")
    if st.button("Show Unpivot example"):
        wide = df.head(60).pivot_table(index=["Date", "Region"], columns="Product", values="Revenue", aggfunc="sum").fillna(0).reset_index()
        st.dataframe(wide.head(10))
        melted = wide.melt(id_vars=["Date", "Region"], var_name="Product", value_name="Revenue")
        st.markdown("Unpivoted (melt) result:")
        st.dataframe(melted.head(10))

    st.markdown("**Merge & Append**")
    st.markdown("Create small examples showing append and merge patterns")
    df_a = df.head(50).copy()
    df_b = df.tail(50).copy()
    if st.button("Show Append example"):
        appended = pd.concat([df_a, df_b], ignore_index=True)
        st.dataframe(appended.head(10))
    if st.button("Show Merge example"):
        lookup = pd.DataFrame({"Product":["Alpha","Beta","Gamma","Delta","Epsilon"], "Category":["C1","C1","C2","C2","C3"]})
        merged = df_a.merge(lookup, on="Product", how="left")
        st.dataframe(merged.head(10))

def page_visualizations():
    st.header("Visualizations & Storytelling")
    st.markdown("Designing clear visuals and telling data stories with charts.")
    df = st.session_state.sample_df.copy()

    st.subheader("Plotly examples")
    fig1 = px.bar(df.groupby("Region")["Revenue"].sum().reset_index(), x="Region", y="Revenue", title="Revenue by Region", template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)
    st.subheader("Altair small multiples example")
    df_small = df.groupby(["Date", "Product"])["Revenue"].sum().reset_index()
    products = df_small["Product"].unique()[:6]
    chart = alt.Chart(df_small[df_small["Product"].isin(products)]).mark_line().encode(
        x="Date:T",
        y="Revenue:Q",
        color="Product:N",
        facet=alt.Facet("Product:N", columns=2)
    ).properties(height=140).configure_title(fontSize=12)
    st.altair_chart(chart, use_container_width=True)

    st.markdown("**Visualization best practices**")
    st.markdown("""
    - Start with a question and choose visuals to answer it.  
    - Avoid chart junk; remove unnecessary grid lines and decorations.  
    - Use color to highlight, not distract.  
    - Use consistent scales for comparison across charts.
    """)

def page_practice_quizzes():
    st.header("Practice & Quizzes")
    st.markdown("Practical exercises with auto-check and progress saving.")

    st.subheader("Exercise 1: Pivot total revenue by region")
    if st.button("Auto-solve Exercise 1"):
        df = st.session_state.sample_df.copy()
        sol = df.groupby("Region").agg(TotalRevenue=("Revenue", "sum")).reset_index()
        st.success("Solution generated")
        st.dataframe(sol)
        excel_download_link(sol, filename="exercise1_solution.xlsx", label="Download solution")
        save_progress(USER_ID, "Practice", "Exercise 1: Pivot by Region", status="complete", score=100)

    st.markdown("---")
    st.subheader("Exercise 2: DAX-like measure")
    st.markdown("Create NetRevenue = Revenue - Discount where Discount = 5% if Price > threshold else 2%")
    threshold = st.number_input("Price threshold for higher discount", value=500, step=50)
    if st.button("Run Exercise 2"):
        df = st.session_state.sample_df.copy()
        df["DiscountPercent"] = np.where(df["Price"] > threshold, 5, 2)
        df["DiscountValue"] = (df["Revenue"] * df["DiscountPercent"] / 100).round(2)
        df["NetRevenue"] = (df["Revenue"] - df["DiscountValue"]).round(2)
        result = df[df["Price"] > threshold]["NetRevenue"].sum().round(2)
        st.info(f"Total NetRevenue for Price > {threshold}: {result}")
        save_progress(USER_ID, "Practice", f"Exercise 2 @ {threshold}", status="complete", score=90)

    st.markdown("---")
    st.subheader("Mini Quiz")
    q1 = st.radio("Q1: Which Power BI component handles data transformations?", ["Data Model", "Power Query", "Report View", "Dashboard"])
    q2 = st.radio("Q2: Which visual is best for part-to-whole comparison?", ["Line", "Scatter", "Pie", "Histogram"])
    if st.button("Submit Quiz"):
        score = 0
        if q1 == "Power Query":
            score += 50
        if q2 == "Pie":
            score += 50
        st.success(f"You scored {score}/100")
        save_progress(USER_ID, "Practice", "Mini Quiz", status="complete", score=score)

def page_templates_cheatsheets():
    st.header("Templates & Cheatsheets")
    st.markdown("Download ready-to-use templates and short reference sheets.")
    df = st.session_state.sample_df.copy()
    monthly = df.copy()
    monthly["Month"] = pd.to_datetime(monthly["Date"]).dt.to_period("M").astype(str)
    monthly_summary = monthly.groupby(["Month", "Region"]).agg(TotalRevenue=("Revenue", "sum"), Units=("Units", "sum")).reset_index()
    st.dataframe(monthly_summary.head(30))
    excel_download_link(monthly_summary, filename="monthly_template.xlsx", label="Download monthly template")
    st.markdown("**Cheatsheet: Common Excel formulas**")
    st.markdown("""
    - SUM(range)  
    - AVERAGE(range)  
    - COUNT / COUNTA  
    - SUMIF / SUMIFS  
    - VLOOKUP / INDEX+MATCH (or XLOOKUP)  
    - IF, AND, OR, ISBLANK
    """)
    st.markdown("**Cheatsheet: Common DAX measures**")
    st.markdown("""
    - Total Revenue = SUM(Table[Revenue])  
    - Average Price = AVERAGE(Table[Price])  
    - Distinct Products = DISTINCTCOUNT(Table[Product])  
    - Revenue YTD = TOTALYTD([Total Revenue], Table[Date])
    """)

def page_profile_progress():
    st.header("Profile & Progress")
    st.markdown(f"User: **{st.session_state.user_name}**")
    dfp = user_progress_summary(USER_ID)
    if dfp.empty:
        st.info("No progress recorded yet. Complete exercises to store progress.")
    else:
        st.dataframe(dfp.sort_values("updated_at", ascending=False))
    st.subheader("Notes")
    title = st.text_input("Note title")
    content = st.text_area("Note content")
    if st.button("Save Note"):
        cur = conn.cursor()
        cur.execute("INSERT INTO notes (user_id, title, content, created_at) VALUES (?, ?, ?, ?)",
                    (USER_ID, title or "Untitled", content or "", datetime.utcnow().isoformat()))
        conn.commit()
        st.success("Note saved.")
    st.subheader("My notes")
    cur = conn.cursor()
    cur.execute("SELECT id, title, created_at FROM notes WHERE user_id = ? ORDER BY created_at DESC", (USER_ID,))
    notes = cur.fetchall()
    if notes:
        for nid, ntitle, ncreated in notes:
            with st.expander(f"{ntitle} • {ncreated}"):
                cur.execute("SELECT content FROM notes WHERE id = ?", (nid,))
                content_row = cur.fetchone()
                if content_row:
                    st.write(content_row[0])
                if st.button(f"Delete note {nid}", key=f"del_{nid}"):
                    cur.execute("DELETE FROM notes WHERE id = ?", (nid,))
                    conn.commit()
                    st.experimental_rerun()

def page_resources_export():
    st.header("Resources & Export")
    st.markdown("Curated external resources and the ability to export your study pack.")
    st.markdown("- Microsoft Excel docs: https://support.microsoft.com/excel")
    st.markdown("- Power BI Learn: https://learn.microsoft.com/power-bi/")
    st.markdown("- Recommended reading: books on data visualization and DAX")
    st.subheader("Export study pack")
    include_sample = st.checkbox("Include sample dataset", value=True)
    include_notes = st.checkbox("Include my notes", value=True)
    include_progress = st.checkbox("Include my progress", value=True)
    if st.button("Generate study pack (separate files)"):
        files = {}
        if include_sample:
            files["sample_dataset.xlsx"] = to_excel_bytes(st.session_state.sample_df)
        if include_notes:
            cur = conn.cursor()
            cur.execute("SELECT title, content, created_at FROM notes WHERE user_id = ?", (USER_ID,))
            rows = cur.fetchall()
            notes_text = "\n\n".join([f"{r[0]} ({r[2]})\n\n{r[1]}" for r in rows]) if rows else "No notes"
            files["notes.txt"] = notes_text.encode("utf-8")
        if include_progress:
            dfp = user_progress_summary(USER_ID)
            files["progress.csv"] = dfp.to_csv(index=False).encode("utf-8")
        for name, data in files.items():
            st.download_button(f"Download {name}", data=data, file_name=name)

# ---------------- Page router ----------------
ROUTER = {
    "Home": page_home,
    "Dataset Explorer": page_dataset_explorer,
    "Excel Basics": page_excel_basics,
    "Excel Advanced": page_excel_advanced,
    "Power BI Basics": page_power_bi_basics,
    "Power BI Advanced": page_power_bi_advanced,
    "Power Query": page_power_query,
    "Visualizations": page_visualizations,
    "Practice & Quizzes": page_practice_quizzes,
    "Templates & Cheatsheets": page_templates_cheatsheets,
    "Profile & Progress": page_profile_progress,
    "Resources & Export": page_resources_export
}

if page in ROUTER:
    try:
        ROUTER[page]()
    except Exception as exc:
        st.error("An error occurred while rendering the page: " + str(exc))
else:
    st.error("Selected page is not implemented.")

# ---------------- Footer ----------------
st.markdown("---")
fcol1, fcol2 = st.columns([3, 1])
with fcol1:
    st.markdown("Built for learning Excel & Power BI. If you'd like additional modules (e.g., Power Automate, advanced DAX courses), request them and they will be added.")
    st.markdown(f"Connect on LinkedIn: [{LINKEDIN_URL}]({LINKEDIN_URL})")
with fcol2:
    st.markdown(f"App generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
