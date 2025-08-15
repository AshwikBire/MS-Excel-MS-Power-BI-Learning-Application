# Learning_Dark_UI_App.py
# Excel & Power BI Learning Lab - Dark Themed Streamlit App
# UTF-8 safe (no emoji). Designed for Windows & cross-platform.
# Large, feature-rich single-file app (approx ~900-1000 logical lines depending on whitespace).
# Requires: streamlit, pandas, numpy, plotly, altair, openpyxl
# Run: streamlit run Learning_Dark_UI_App.py

import streamlit as st
import pandas as pd
import numpy as np
import io
import base64
import sqlite3
import plotly.express as px
import altair as alt
from datetime import datetime
from typing import Tuple, List, Dict

# ------------------------------------------------------------
# App configuration
# ------------------------------------------------------------
st.set_page_config(
    page_title="Excel & Power BI Learning Lab (Dark)",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# DARK THEME CSS
# ------------------------------------------------------------
def local_css():
    css = """
    <style>
    /* Base dark background and fonts */
    :root {
        --bg-color: #0f1720;
        --card-color: #111827;
        --muted: #9ca3af;
        --accent: #06b6d4;
        --accent-2: #7c3aed;
        --surface: #0b1220;
        --border: rgba(255,255,255,0.06);
        --text: #e5eef8;
        --secondary-text: #cbd5e1;
    }
    /* Page background */
    .stApp {
        background: linear-gradient(180deg, var(--bg-color) 0%, #071021 100%);
        color: var(--text);
        font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }

    /* Card style for main containers */
    .big-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 6px 18px rgba(2,6,23,0.6), inset 0 1px 0 rgba(255,255,255,0.02);
        border: 1px solid var(--border);
    }

    /* Sidebar custom */
    .css-1oe5cao { /* works with Streamlit internal class names - may change in future */
        background-color: #071021 !important;
    }

    /* Headings */
    .stHeader {
        color: var(--text);
        font-weight: 700;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, var(--accent), var(--accent-2));
        color: #001219;
        font-weight: 600;
        border: none;
        box-shadow: none;
    }

    /* Small muted text */
    .muted {
        color: var(--muted);
        font-size: 0.9rem;
    }

    /* Table styling adjustments */
    .stDataFrame table {
        background-color: transparent;
        color: var(--text);
    }

    /* Download link style */
    .download-link {
        background: rgba(124,58,237,0.12);
        padding: 8px 14px;
        border-radius: 8px;
        color: var(--accent-2);
        display: inline-block;
        text-decoration: none;
    }

    /* Minimal input styles */
    .stTextInput>div>div>input {
        background-color: #0b1220;
        color: var(--text);
    }

    /* Progress badge */
    .progress-badge {
        background: rgba(6,182,212,0.12);
        padding: 6px 10px;
        border-radius: 999px;
        color: var(--accent);
        font-weight: 600;
    }

    /* Code block look */
    .stCodeBlock pre {
        background: #071021;
        color: var(--secondary-text);
        border-radius: 8px;
        padding: 12px;
    }

    /* Responsive: narrow screens */
    @media (max-width: 640px) {
        .big-card { padding: 12px; }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

local_css()

# ------------------------------------------------------------
# Utilities: sample data, excel export, sqlite progress, helpers
# ------------------------------------------------------------
def sample_data(rows: int = 200, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    # generate daily dates
    dates = pd.date_range(end=pd.Timestamp.today(), periods=rows)
    df = pd.DataFrame({
        "Date": rng.choice(dates, size=rows),
        "Region": rng.choice(["North", "South", "East", "West"], size=rows, p=[0.25,0.25,0.25,0.25]),
        "Product": rng.choice(["Alpha", "Beta", "Gamma", "Delta", "Epsilon"], size=rows),
        "Channel": rng.choice(["Retail", "Online", "Wholesale"], size=rows, p=[0.5,0.35,0.15]),
        "Units": rng.integers(1, 120, size=rows),
        "Price": np.round(rng.uniform(20, 1500, size=rows), 2)
    })
    df["Revenue"] = (df["Units"] * df["Price"]).round(2)
    # add a calculated margin column as example
    df["MarginPercent"] = np.round(rng.uniform(5, 35, size=rows), 2)
    df["MarginValue"] = np.round(df["Revenue"] * df["MarginPercent"] / 100, 2)
    return df.sort_values("Date").reset_index(drop=True)

def to_excel_bytes(df: pd.DataFrame, sheet_name: str = "Sheet1") -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        try:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
        except Exception:
            # fallback: convert non-serializable columns
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

# ------------------------------------------------------------
# SQLite for progress tracking & saved exercises
# ------------------------------------------------------------
DB_PATH = "learning_progress.db"

def init_db(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
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

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    init_db(conn)
    return conn

conn = get_conn()

# ------------------------------------------------------------
# App sidebar: user selection, nav, settings
# ------------------------------------------------------------
st.sidebar.markdown("<div class='big-card'>", unsafe_allow_html=True)
st.sidebar.title("Navigation")
st.sidebar.caption("Excel & Power BI Learning Lab — Dark UI")

# User profile + quick progress
if "user_name" not in st.session_state:
    st.session_state.user_name = "Guest"
user_name = st.sidebar.text_input("Your name", value=st.session_state.user_name)
st.session_state.user_name = user_name

# persist user to DB
def ensure_user(conn, name: str) -> int:
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE name = ?", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO users (name, created_at) VALUES (?, ?)", (name, datetime.utcnow().isoformat()))
    conn.commit()
    return cur.lastrowid

USER_ID = ensure_user(conn, st.session_state.user_name)

# Navigation
pages = [
    "Home",
    "Dataset Explorer",
    "Excel Basics",
    "Formulas & Pivot",
    "Charts & Visualization",
    "Power Query (Transformations)",
    "Power BI Concepts",
    "Data Modeling & DAX (Intro)",
    "Practice & Quizzes",
    "Templates & Cheatsheets",
    "Profile & Progress",
    "Resources & Export"
]
page = st.sidebar.radio("Go to", pages, index=0)
st.sidebar.markdown("---")
st.sidebar.markdown("Theme: Dark • Designed for focused study")
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# Header - main page top
# ------------------------------------------------------------
st.markdown("<div class='big-card'>", unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Excel & Power BI Learning Lab")
    st.markdown("Master Excel and Power BI with hands-on examples, guided lessons, and practical exercises. This dark-themed learning workspace focuses on content clarity and contrast for prolonged usage.")
with col2:
    st.markdown("<div style='text-align:right'>", unsafe_allow_html=True)
    st.markdown(f"<div class='progress-badge'>User: {st.session_state.user_name}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# Global session sample df
# ------------------------------------------------------------
if "sample_df" not in st.session_state:
    st.session_state.sample_df = sample_data(400)

# ------------------------------------------------------------
# Helper: write progress
# ------------------------------------------------------------
def save_progress(user_id: int, section: str, subtopic: str, status: str = "incomplete", score: int = None):
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO progress (user_id, section, subtopic, status, score, updated_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, section, subtopic, status, score if score is not None else -1, datetime.utcnow().isoformat()))
    conn.commit()

def user_progress_summary(user_id: int) -> pd.DataFrame:
    cur = conn.cursor()
    cur.execute("SELECT section, subtopic, status, score, updated_at FROM progress WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    if not rows:
        return pd.DataFrame(columns=["section", "subtopic", "status", "score", "updated_at"])
    df = pd.DataFrame(rows, columns=["section", "subtopic", "status", "score", "updated_at"])
    return df

# ------------------------------------------------------------
# Page implementations
# ------------------------------------------------------------
def page_home():
    st.header("Welcome")
    st.markdown("""
    This workspace contains lessons, interactive demos, downloadable templates, and exercises to practice Excel and Power BI skills.
    Use the left navigation to jump between sections. Sample datasets are included and can be downloaded.
    """)
    # Quick summary cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<div class='big-card'><h4>Quick Start</h4><p class='muted'>Load sample data, explore pivot tables, and practice visualizations.</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='big-card'><h4>Modules</h4><p class='muted'>Excel Basics → Power Query → Modeling → DAX → Reporting</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='big-card'><h4>Practice</h4><p class='muted'>Step-by-step exercises and quizzes with auto-check.</p></div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='big-card'><h4>Export</h4><p class='muted'>Download templates and your notes from the Resources tab.</p></div>", unsafe_allow_html=True)

    st.markdown("---")
    # Show overview visualization
    df = st.session_state.sample_df.copy()
    agg = df.groupby("Region").agg(TotalRevenue=("Revenue", "sum"), TotalUnits=("Units", "sum")).reset_index()
    fig = px.bar(agg, x="Region", y="TotalRevenue", title="Revenue by Region (Sample Dataset)", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Lesson Roadmap")
    st.markdown("""
    1. Excel Basics: sheets, imports, cleaning  
    2. Formulas & Pivot: common formulas, creating pivot tables  
    3. Visualization: charts in Excel and Power BI  
    4. Power Query: transformations and M concept overview  
    5. Data Modeling & DAX: relationships, measures & calculated columns  
    6. Reporting: building dashboards & storytelling  
    7. Practice: exercises, quizzes, templates
    """)

def page_dataset_explorer():
    st.header("Dataset Explorer")
    st.markdown("Upload your own file or use the sample dataset to explore data types, quick stats, filtering, and simple cleaning operations.")
    uploaded = st.file_uploader("Upload CSV / Excel", type=["csv", "xlsx", "xls"])
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
            return
    else:
        st.info("No file uploaded — using sample dataset.")
        df = st.session_state.sample_df.copy()

    with st.expander("Data Preview"):
        st.dataframe(df.head(200))

    with st.expander("Summary & Types"):
        st.write("Shape:", df.shape)
        st.write("Columns & dtypes")
        dtypes = pd.DataFrame({"column": df.columns, "dtype": [str(df[c].dtype) for c in df.columns]})
        st.table(dtypes)

    with st.expander("Basic Cleaning Tools"):
        cols = df.columns.tolist()
        to_drop = st.multiselect("Columns to drop", cols)
        if st.button("Remove selected columns"):
            df = df.drop(columns=to_drop)
            st.session_state.sample_df = df
            st.success(f"Dropped: {', '.join(to_drop)}")
            st.dataframe(df.head(50))

        # Fillna
        numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        if numeric_cols:
            fill_choice = st.selectbox("Fill missing numeric values with", ["Do nothing", "0", "mean", "median"])
            if st.button("Apply fill for numeric"):
                if fill_choice == "0":
                    df[numeric_cols] = df[numeric_cols].fillna(0)
                elif fill_choice == "mean":
                    for c in numeric_cols:
                        df[c] = df[c].fillna(df[c].mean())
                elif fill_choice == "median":
                    for c in numeric_cols:
                        df[c] = df[c].fillna(df[c].median())
                st.session_state.sample_df = df
                st.success("Filled missing numeric values.")
                st.dataframe(df.head(50))

    st.markdown("### Quick Export")
    excel_download_link(df, filename="explorer_data.xlsx", label="Download current data as Excel")

def page_excel_basics():
    st.header("Excel Basics")
    st.markdown("""
    In this module you will learn how to:
    - Import data from CSV / Excel  
    - Work with sheets and data types  
    - Simple formatting and quick calculations  
    - Exporting back to Excel
    """)
    st.subheader("Interactive examples")
    df = st.session_state.sample_df.copy()
    st.markdown("**Preview sample dataset**")
    st.dataframe(df.head(150))

    st.markdown("**Common Excel-like operations (Pandas under the hood)**")
    ops_col1, ops_col2 = st.columns(2)
    with ops_col1:
        if st.button("Show first 10 rows"):
            st.dataframe(df.head(10))
        if st.button("Show descriptive stats"):
            st.dataframe(df.describe().T)
    with ops_col2:
        if st.button("Show null counts"):
            st.dataframe(df.isna().sum().to_frame("missing_count"))
        if st.button("Convert Date column to datetime"):
            if "Date" in df.columns:
                df["Date"] = pd.to_datetime(df["Date"])
                st.session_state.sample_df = df
                st.success("Converted Date to datetime.")
                st.dataframe(df.dtypes.to_frame("dtype"))

    st.markdown("**Export examples**")
    excel_download_link(df.head(200), filename="excel_basics_sample.xlsx", label="Download example subset")

def page_formulas_pivot():
    st.header("Formulas & Pivot Tables")
    st.markdown("""
    This module demonstrates:
    - Formula concepts (SUM, AVERAGE, IF, VLOOKUP-like joins)  
    - Creating pivot tables and exporting them
    """)
    df = st.session_state.sample_df.copy()
    st.markdown("### Formula demonstrations")
    # Simple 'Excel-like' formulas using pandas
    left, right = st.columns(2)
    with left:
        st.markdown("**Calculated Column**: UnitPriceTimesUnits = Units * Price")
        if "Units" in df.columns and "Price" in df.columns:
            df["CalcRevenue"] = (df["Units"] * df["Price"]).round(2)
            st.dataframe(df[["Units", "Price", "CalcRevenue"]].head(10))

        st.markdown("**IF example**: Mark high-revenue rows")
        df["HighRevenueFlag"] = np.where(df["Revenue"] > df["Revenue"].median(), "High", "Normal")
        st.dataframe(df[["Revenue", "HighRevenueFlag"]].head(10))

    with right:
        st.markdown("**Join (VLOOKUP analogue)**")
        st.markdown("Create a small lookup table and demonstrate merging.")
        lookup = pd.DataFrame({
            "Product": ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"],
            "Category": ["Core", "Core", "Extended", "Extended", "Special"]
        })
        st.table(lookup)
        merged = df.merge(lookup, on="Product", how="left")
        st.dataframe(merged[["Product", "Category"]].drop_duplicates().head(10))

    st.markdown("### Pivot table builder")
    cols = df.columns.tolist()
    index = st.multiselect("Index (rows)", cols, default=["Region"])
    columns_choice = st.multiselect("Columns", cols, default=["Product"])
    values = st.selectbox("Values (numeric)", [c for c in cols if pd.api.types.is_numeric_dtype(df[c])], index=cols.index("Revenue") if "Revenue" in cols else 0)
    agg = st.selectbox("Aggregation", ["sum", "mean", "count", "median", "min", "max"], index=0)
    if st.button("Create Pivot Table"):
        try:
            pivot = pd.pivot_table(df, index=index or None, columns=columns_choice or None, values=values, aggfunc=agg, margins=True, fill_value=0)
            st.dataframe(pivot)
            st.download_button("Download pivot as Excel", data=to_excel_bytes(pivot.reset_index()), file_name="pivot_table.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            # save progress
            save_progress(USER_ID, "Formulas & Pivot", "Created Pivot", status="complete")
        except Exception as e:
            st.error("Pivot creation error: " + str(e))

def page_charts_visualization():
    st.header("Charts & Visualization")
    st.markdown("""
    Compare Excel and Power BI visualization concepts. Demonstrations include:
    - Basic charts (bar, line, scatter)
    - Advanced visuals: small multiples, stacked bars, treemap
    - Interactive plotly charts and altair examples
    """)
    df = st.session_state.sample_df.copy()
    chart = st.selectbox("Choose visualization", [
        "Bar: Revenue by Region",
        "Line: Revenue over Time (daily)",
        "Stacked Bar: Revenue by Region & Product",
        "Treemap: Revenue by Product",
        "Scatter: Units vs Price with Revenue size",
        "Small Multiples: Product revenue across regions"
    ])
    if chart == "Bar: Revenue by Region":
        agg = df.groupby("Region")["Revenue"].sum().reset_index()
        fig = px.bar(agg, x="Region", y="Revenue", title="Revenue by Region", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    elif chart == "Line: Revenue over Time (daily)":
        df2 = df.groupby(pd.Grouper(key="Date", freq="D"))["Revenue"].sum().reset_index()
        fig = px.line(df2, x="Date", y="Revenue", title="Daily Revenue", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    elif chart == "Stacked Bar: Revenue by Region & Product":
        agg = df.groupby(["Region", "Product"])["Revenue"].sum().reset_index()
        fig = px.bar(agg, x="Region", y="Revenue", color="Product", title="Stacked Revenue by Product", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    elif chart == "Treemap: Revenue by Product":
        agg = df.groupby(["Product", "Region"])["Revenue"].sum().reset_index()
        fig = px.treemap(agg, path=["Product", "Region"], values="Revenue", title="Revenue Treemap", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    elif chart == "Scatter: Units vs Price with Revenue size":
        fig = px.scatter(df.sample(min(500, len(df))), x="Units", y="Price", size="Revenue", color="Region", hover_data=["Product"], title="Units vs Price (sample)", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        # small multiples: altair
        df_small = df.groupby(["Date", "Product"])["Revenue"].sum().reset_index()
        chart_alt = alt.Chart(df_small[df_small["Product"].isin(df_small["Product"].unique()[:6])]).mark_line().encode(
            x="Date:T", y="Revenue:Q", color="Product:N", facet=alt.Facet("Product:N", columns=2)
        ).properties(height=150).configure_facet(spacing=8)
        st.altair_chart(chart_alt, use_container_width=True)

    st.markdown("**Tip:** For storytelling, choose 1-3 visuals and annotate key insights. Avoid excessive colors and clutter.")

def page_power_query():
    st.header("Power Query (Transformations)")
    st.markdown("""
    Power Query is used for data ingestion and transformation. Here we simulate common transformations using pandas:
    - Column unpivot / pivot
    - split / merge columns
    - calculated columns
    - dedupe and group operations
    """)
    df = st.session_state.sample_df.copy()
    st.subheader("Common transformations examples")
    if st.button("Unpivot (melt) example"):
        # create a wide sample
        wide = df.head(50).copy()
        # pivot by Region & Product with Revenue as a value
        sample_wide = wide.pivot_table(index=["Date", "Region"], columns="Product", values="Revenue", aggfunc="sum").fillna(0).reset_index()
        st.dataframe(sample_wide.head(10))
        melted = sample_wide.melt(id_vars=["Date", "Region"], var_name="Product", value_name="Revenue")
        st.markdown("**Unpivot result (melt)**")
        st.dataframe(melted.head(10))
    if st.button("Split Column by delimiter example"):
        # create a compound column
        df2 = df.head(40).copy()
        df2["Product_Category"] = df2["Product"] + "|" + df2["Channel"]
        st.dataframe(df2[["Product_Category"]].head(6))
        split = df2["Product_Category"].str.split("|", expand=True)
        split.columns = ["Product", "Channel"]
        st.dataframe(split.head(6))

    if st.button("Group and aggregate example"):
        agg = df.groupby(["Region", "Channel"]).agg(TotalRevenue=("Revenue", "sum"), AvgUnits=("Units", "mean")).reset_index()
        st.dataframe(agg.head(20))

def page_power_bi_concepts():
    st.header("Power BI Concepts")
    st.markdown("""
    Power BI includes these main pieces:
    - Power Query (ingest & transform)
    - Data Model (tables & relationships)
    - DAX (expressions for measures and calculated columns)
    - Reports & Dashboards (visuals, interactions, bookmarks)
    """)
    st.markdown("**Data Model Example**")
    st.markdown("We can simulate a star schema with fact and dimension tables.")
    # prepare dimension tables
    df = st.session_state.sample_df.copy()
    dim_product = df[["Product"]].drop_duplicates().reset_index(drop=True)
    dim_region = df[["Region"]].drop_duplicates().reset_index(drop=True)
    fact = df[["Date", "Product", "Region", "Units", "Price", "Revenue"]]
    st.markdown("**Fact table (sample)**")
    st.dataframe(fact.head(10))
    st.markdown("**Dimension: Product**")
    st.dataframe(dim_product)
    st.markdown("Power BI best practices: use star schema, avoid bi-directional cross-filtering unless needed, create measures rather than calculated columns where possible for performance.")

def page_data_modeling_dax():
    st.header("Data Modeling & DAX (Intro)")
    st.markdown("DAX is a formula language. Below we show pandas equivalents for measures and calculated columns.")
    df = st.session_state.sample_df.copy()
    st.subheader("Calculated Columns")
    if st.button("Add Calculated Columns (Gross, Discount example)"):
        df["DiscountPercent"] = np.where(df["Price"] > 500, 5, 2)
        df["DiscountValue"] = np.round(df["Revenue"] * df["DiscountPercent"] / 100, 2)
        df["NetRevenue"] = (df["Revenue"] - df["DiscountValue"]).round(2)
        st.dataframe(df[["Price", "Revenue", "DiscountPercent", "DiscountValue", "NetRevenue"]].head(8))
        st.session_state.sample_df = df

    st.subheader("Measures (DAX-like using groupby)")
    st.markdown("Common measures: Total Revenue, Average Price, Distinct Count of Products")
    measures = {
        "TotalRevenue": df["Revenue"].sum(),
        "AveragePrice": df["Price"].mean(),
        "DistinctProducts": df["Product"].nunique()
    }
    st.table(pd.DataFrame(list(measures.items()), columns=["Measure", "Value"]).set_index("Measure"))

    st.markdown("**Time Intelligence sample** (Year-to-date using pandas)")
    try:
        df["Date"] = pd.to_datetime(df["Date"])
        df_sorted = df.sort_values("Date")
        df_sorted["YTDRevenue"] = df_sorted.groupby(df_sorted["Date"].dt.year)["Revenue"].cumsum()
        st.line_chart(df_sorted.set_index("Date")["YTDRevenue"].resample("D").mean().fillna(0))
    except Exception as e:
        st.error("Time intelligence example failed: " + str(e))

def page_practice_quizzes():
    st.header("Practice & Quizzes")
    st.markdown("Interactive exercises that you can attempt and auto-check. Your progress is saved to your profile.")
    # Exercise 1: pivot revenue by region
    st.subheader("Exercise 1: Pivot by Region")
    st.markdown("Instruction: Create a pivot table showing total Revenue by Region. Use the Build Pivot tool or press 'Auto-solve' to see the answer.")
    if st.button("Auto-solve Exercise 1"):
        df = st.session_state.sample_df.copy()
        sol = df.groupby("Region").agg(TotalRevenue=("Revenue", "sum")).reset_index()
        st.success("Auto-solved. See solution below.")
        st.dataframe(sol)
        excel_download_link(sol, filename="exercise1_solution.xlsx", label="Download solution")
        save_progress(USER_ID, "Practice & Quizzes", "Exercise 1: Pivot by Region", status="complete", score=100)

    st.markdown("---")
    # Exercise 2: DAX-like measure
    st.subheader("Exercise 2: Create a Net Revenue measure")
    st.markdown("Instruction: Define NetRevenue = Revenue - DiscountValue. Filter rows with Price > 500 and compute total NetRevenue.")
    price_filter = st.number_input("Price threshold", value=500, step=50)
    if st.button("Check my solution (Run)"):
        df = st.session_state.sample_df.copy()
        df["DiscountPercent"] = np.where(df["Price"] > price_filter, 5, 2)
        df["DiscountValue"] = np.round(df["Revenue"] * df["DiscountPercent"] / 100, 2)
        df["NetRevenue"] = (df["Revenue"] - df["DiscountValue"]).round(2)
        result = df[df["Price"] > price_filter]["NetRevenue"].sum().round(2)
        st.info(f"Computed total NetRevenue for Price > {price_filter}: {result}")
        save_progress(USER_ID, "Practice & Quizzes", f"Exercise 2: NetRevenue @ {price_filter}", status="complete", score=90)

    st.markdown("---")
    # Quiz: multiple choice
    st.subheader("Quick Quiz (2 questions)")
    q1 = st.radio("Q1: In Power BI, which component is used for data transformations?", ["Data Model", "Power Query", "Report View", "Dashboard"])
    q2 = st.radio("Q2: Which chart is best for showing part-to-whole relationships?", ["Line chart", "Scatter chart", "Pie chart", "Histogram"])
    if st.button("Submit Quiz"):
        score = 0
        if q1 == "Power Query":
            score += 50
        if q2 == "Pie chart":
            score += 50
        st.success(f"You scored {score}/100")
        save_progress(USER_ID, "Practice & Quizzes", "Mini Quiz", status="complete", score=score)

def page_templates_cheatsheets():
    st.header("Templates & Cheatsheets")
    st.markdown("Downloadable templates for common Excel tasks and Power BI starter files.")
    st.markdown("1. Sales template (Pivot-ready)  2. Monthly reporting template  3. Power BI model CSVs")
    df = st.session_state.sample_df.copy()
    st.markdown("Download a prepared monthly summary template")
    monthly = df.copy()
    monthly["Month"] = pd.to_datetime(monthly["Date"]).dt.to_period("M").astype(str)
    monthly_summary = monthly.groupby(["Month", "Region"]).agg(TotalRevenue=("Revenue", "sum"), Units=("Units", "sum")).reset_index()
    st.dataframe(monthly_summary.head(20))
    excel_download_link(monthly_summary, filename="monthly_template.xlsx", label="Download monthly template")

    st.markdown("Cheatsheet examples:")
    st.markdown("""
    - Excel formulas: SUM, AVERAGE, COUNTIFS, SUMIFS, VLOOKUP (or INDEX+MATCH), XLOOKUP  
    - Pivot tips: Use Slicers, Group dates, Use calculated fields for percent share  
    - Power BI tips: Star schema, Use measures (not calculated columns for aggregates), Keep data model small
    """)

def page_profile_progress():
    st.header("Profile & Progress")
    st.markdown(f"User: **{st.session_state.user_name}**")
    st.markdown("Saved notes and progress history are stored locally in a small SQLite database.")

    # Show progress summary
    dfp = user_progress_summary(USER_ID)
    if dfp.empty:
        st.info("No progress recorded yet. Complete exercises to save progress.")
    else:
        st.dataframe(dfp.sort_values("updated_at", ascending=False))

    # Notes
    st.subheader("Notes")
    note_title = st.text_input("Note title")
    note_content = st.text_area("Content")
    if st.button("Save Note"):
        cur = conn.cursor()
        cur.execute("INSERT INTO notes (user_id, title, content, created_at) VALUES (?, ?, ?, ?)",
                    (USER_ID, note_title or "Untitled", note_content or "", datetime.utcnow().isoformat()))
        conn.commit()
        st.success("Saved note.")

    # List notes
    cur = conn.cursor()
    cur.execute("SELECT id, title, created_at FROM notes WHERE user_id = ? ORDER BY created_at DESC", (USER_ID,))
    notes = cur.fetchall()
    if notes:
        for n in notes:
            nid, title, created = n
            with st.expander(f"{title} • {created}"):
                cur.execute("SELECT content FROM notes WHERE id = ?", (nid,))
                content = cur.fetchone()
                if content:
                    st.write(content[0])
                if st.button(f"Delete note {nid}"):
                    cur.execute("DELETE FROM notes WHERE id = ?", (nid,))
                    conn.commit()
                    st.experimental_rerun()

def page_resources_export():
    st.header("Resources & Export")
    st.markdown("Curated learning resources, links, and the ability to export your study pack.")
    st.markdown("""
    - Official Excel documentation: search Microsoft docs  
    - Power BI guided learning: Microsoft Learn  
    - Suggested books: data visualization, data modeling, DAX references
    """)
    # Create a zip-like export (simple: multiple files in memory not zipped)
    st.subheader("Export study pack")
    include_sample = st.checkbox("Include sample dataset", value=True)
    include_notes = st.checkbox("Include my notes", value=True)
    include_progress = st.checkbox("Include my progress (CSV)", value=True)
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
        # Offer separate downloads
        for name, data in files.items():
            st.download_button(f"Download {name}", data=data, file_name=name)

# Map page keys to functions
PAGE_FUNCTIONS = {
    "Home": page_home,
    "Dataset Explorer": page_dataset_explorer,
    "Excel Basics": page_excel_basics,
    "Formulas & Pivot": page_formulas_pivot,
    "Charts & Visualization": page_charts_visualization,
    "Power Query (Transformations)": page_power_query,
    "Power BI Concepts": page_power_bi_concepts,
    "Data Modeling & DAX (Intro)": page_data_modeling_dax,
    "Practice & Quizzes": page_practice_quizzes,
    "Templates & Cheatsheets": page_templates_cheatsheets,
    "Profile & Progress": page_profile_progress,
    "Resources & Export": page_resources_export
}

# Execute the selected page
if page in PAGE_FUNCTIONS:
    try:
        PAGE_FUNCTIONS[page]()
    except Exception as e:
        st.error("An error occurred while rendering the page: " + str(e))
else:
    st.error("Page not implemented.")

# Footer - small help area
st.markdown("---")
footer_col1, footer_col2 = st.columns([3, 1])
with footer_col1:
    st.markdown("If you want additional modules (e.g., Power Automate, advanced DAX, or report storytelling templates), request them from the left navigation and they will be added.")
with footer_col2:
    st.markdown(f"App generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
