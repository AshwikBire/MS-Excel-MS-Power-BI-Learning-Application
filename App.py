-- coding: utf-8 --

Excel + Power BI Learning App (Colorful One-Page Tabs)

Excel + Power BI Learning App (Colorful One-Page Tabs)

-----------------------------------------------------

Single-file Streamlit application with colorful, single-page tab UI.

No external APIs required. Pure Python + common data/plot libs.



Features

- Vibrant themed UI with dynamic accent picker

- Single page with colored tabs (Excel, Power BI, DAX, Power Query, Charts, Datasets, Projects, Quiz, Shortcuts, Cheat Sheets, Roadmaps, Resources)

- 1500-ish lines of code packed with curated content, tips, and interactive demos

- Interactive quizzes with instant scoring and explanations

- Mini labs for Excel functions & DAX translated to pandas/Altair examples

- Visualization gallery and style templates

- Downloadable notes/cheatsheets generated on the fly

- Lightweight certificate of completion generator (PNG) after passing quiz

- Everything runs locally; no API keys



Notes

- Streamlit versions after 1.25 support tabs CSS class names used here; if yours is older,

update Streamlit to see all visual styles.

- You can safely comment/uncomment sections to trim features.

from future import annotations import streamlit as st import pandas as pd import numpy as np import altair as alt import textwrap import io from datetime import datetime, date import base64 import random from dataclasses import dataclass

---------------------------------------------

Page Config

---------------------------------------------

st.set_page_config( page_title="Excel + Power BI Learning - Colorful Tabs", page_icon="📊", layout="wide", initial_sidebar_state="collapsed", )

---------------------------------------------

Utility: Accent / Theme Manager (dynamic CSS)

---------------------------------------------

DEFAULT_ACCENT = "#8A2BE2"  # blueviolet ACCENTS = { "Aurora": "#8A2BE2", "Mango": "#FF8C00", "Lagoon": "#00B3B3", "Rose": "#FF3B7F", "Lime": "#39D353", "Ocean": "#1E90FF", "Sunset": "#FF6B6B", "Amethyst": "#9966FF", "Coral": "#FF7F50", "Teal": "#2AB3A6", }

if "accent" not in st.session_state: st.session_state.accent = DEFAULT_ACCENT if "username" not in st.session_state: st.session_state.username = "Ashwik Bire" if "passed_quiz" not in st.session_state: st.session_state.passed_quiz = False

def inject_css(accent: str): """Inject colorful CSS for the whole app, including per-tab colors.""" # Tab palette (cyclic). We color the first 12 tabs uniquely. tab_colors = [ "linear-gradient(135deg, #8A2BE2 0%, #6A5ACD 100%)", "linear-gradient(135deg, #FF8C00 0%, #FF6B6B 100%)", "linear-gradient(135deg, #00B3B3 0%, #1E90FF 100%)", "linear-gradient(135deg, #39D353 0%, #2AB3A6 100%)", "linear-gradient(135deg, #FF3B7F 0%, #FF7F50 100%)", "linear-gradient(135deg, #9966FF 0%, #8A2BE2 100%)", "linear-gradient(135deg, #1E90FF 0%, #00BFFF 100%)", "linear-gradient(135deg, #FF6B6B 0%, #FFA07A 100%)", "linear-gradient(135deg, #2AB3A6 0%, #20C997 100%)", "linear-gradient(135deg, #FFD166 0%, #FF8C00 100%)", "linear-gradient(135deg, #6EE7B7 0%, #3B82F6 100%)", "linear-gradient(135deg, #F472B6 0%, #8B5CF6 100%)", ]

css = f"""
<style>
:root {{
    --accent: {accent};
    --card-bg: rgba(255,255,255,0.06);
    --card-border: rgba(255,255,255,0.15);
    --text: #f6f6f9;
    --muted: #cfd3dc;
    --shadow: 0 10px 20px rgba(0,0,0,0.25);
}}
.stApp {{
    background: radial-gradient(1200px 800px at 12% -10%, rgba(138,43,226,0.25), transparent 60%),
                radial-gradient(1200px 800px at 110% 10%, rgba(30,144,255,0.25), transparent 60%),
                linear-gradient(135deg, #0f1226, #0b1020 40%, #0a0d1a);
    color: var(--text);
}}
/* Headings */
h1, h2, h3, h4 {{ color: var(--text); }}
/* Accent underlines */
.headline {{
    position: relative;
    padding-bottom: .35rem;
    display: inline-block;
}}
.headline:after {{
    content:"";
    position:absolute; left:0; bottom:0; height:3px; width:100%;
    background: linear-gradient(90deg, var(--accent), transparent);
    border-radius: 3px;
}}
/* Cards */
.card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 18px;
    padding: 16px 18px;
    box-shadow: var(--shadow);
    transition: transform .15s ease, background .2s ease, border .2s ease;
    backdrop-filter: blur(6px);
}}
.card:hover {{ transform: translateY(-2px); border-color: var(--accent); }}

/* Buttons */
.stButton>button {{
    background: var(--accent) !important;
    color: white !important;
    border: 0 !important; border-radius: 12px !important; font-weight: 600 !important;
    box-shadow: var(--shadow) !important;
}}

/* Tabs */
.stTabs [role="tablist"] {{ gap: .35rem; }}
.stTabs [role="tab"] {{
    background: rgba(255,255,255,0.08);
    border-radius: 14px; padding: 10px 16px; font-weight: 700; color: #f5f7ff;
    border: 1px solid rgba(255,255,255,0.12);
}}
.stTabs [role="tab"][aria-selected="true"] {{
    border-color: var(--accent);
    box-shadow: var(--shadow);
}}
/* Per-tab unique gradients via nth-child */
.stTabs [role="tablist"] > div:nth-child(1) button {{ background: {tab_colors[0]}; }}
.stTabs [role="tablist"] > div:nth-child(2) button {{ background: {tab_colors[1]}; }}
.stTabs [role="tablist"] > div:nth-child(3) button {{ background: {tab_colors[2]}; }}
.stTabs [role="tablist"] > div:nth-child(4) button {{ background: {tab_colors[3]}; }}
.stTabs [role="tablist"] > div:nth-child(5) button {{ background: {tab_colors[4]}; }}
.stTabs [role="tablist"] > div:nth-child(6) button {{ background: {tab_colors[5]}; }}
.stTabs [role="tablist"] > div:nth-child(7) button {{ background: {tab_colors[6]}; }}
.stTabs [role="tablist"] > div:nth-child(8) button {{ background: {tab_colors[7]}; }}
.stTabs [role="tablist"] > div:nth-child(9) button {{ background: {tab_colors[8]}; }}
.stTabs [role="tablist"] > div:nth-child(10) button {{ background: {tab_colors[9]}; }}
.stTabs [role="tablist"] > div:nth-child(11) button {{ background: {tab_colors[10]}; }}
.stTabs [role="tablist"] > div:nth-child(12) button {{ background: {tab_colors[11]}; }}

/* Badges */
.badge {{ display:inline-block; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:700; border:1px solid rgba(255,255,255,0.2); }}

/* Subtle separators */
.divider {{ height:1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent); margin: 12px 0; }}

/* Tables */
.rownote {{ color: var(--muted); font-size: 12px; }}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

inject_css(st.session_state.accent)

---------------------------------------------

Header: App Title + Accent Picker

---------------------------------------------

col_a, col_b = st.columns([0.75, 0.25]) with col_a: st.markdown( f""" <h1 class='headline'>📘 Excel + 📊 Power BI Learning Hub</h1> <div class='rownote'>Colorful one-page app • Interactive labs • Quizzes • Cheatsheets • Projects</div> """, unsafe_allow_html=True, ) with col_b: theme = st.selectbox("Pick Accent Theme", list(ACCENTS.keys()), index=list(ACCENTS.keys()).index("Aurora")) if ACCENTS[theme] != st.session_state.accent: st.session_state.accent = ACCENTS[theme] inject_css(st.session_state.accent)

---------------------------------------------

Helper: Download bytes/text

---------------------------------------------

def make_download_button(label: str, data: bytes, file_name: str, help: str | None = None): st.download_button(label, data=data, file_name=file_name, mime="application/octet-stream", help=help)

def df_to_csv_bytes(df: pd.DataFrame) -> bytes: return df.to_csv(index=False).encode("utf-8")

---------------------------------------------

Example Data / Demos

---------------------------------------------

np.random.seed(13) people = ["Aarav", "Isha", "Vihaan", "Diya", "Kabir", "Anaya", "Advait", "Myra", "Vivaan", "Sara"] regions = ["North", "South", "East", "West"] months = pd.date_range("2024-01-01", periods=12, freq="MS").strftime("%b").tolist()

sales_rows = [] for m in months: for p in people: row = { "Month": m, "Person": p, "Region": random.choice(regions), "Units": random.randint(5, 60), "Price": random.choice([99, 199, 299, 399, 499]), } row["Revenue"] = row["Units"] * row["Price"] sales_rows.append(row)

sales_df = pd.DataFrame(sales_rows)

Mini HR dataset

hr_df = pd.DataFrame({ "Employee": [f"E{i:03d}" for i in range(1, 101)], "Dept": np.random.choice(["Finance", "Sales", "Ops", "HR", "IT"], 100), "Level": np.random.choice(["Junior", "Mid", "Senior"], 100, p=[0.5, 0.35, 0.15]), "Salary": np.random.randint(30000, 180000, 100), "JoinDate": pd.to_datetime(np.random.choice(pd.date_range("2019-01-01", "2025-08-01"), 100)), "Performance": np.random.choice(["A", "B", "C"], 100, p=[0.2, 0.6, 0.2]) })

---------------------------------------------

Content Blocks / Knowledge

---------------------------------------------

EXCEL_TIPS = [ "Use Ctrl+; for today's date and Ctrl+Shift+; for current time.", "Ctrl+T converts a range to a Table - unlocks structured refs & quick slicers.", "Alt, H, O, I auto-fits column width (sequential key tips).", "Use Data > Remove Duplicates after selecting relevant columns.", "Name ranges (Formulas > Name Manager) for readable formulas.", "Use F4 to toggle absolute/relative refs ($A$1).", "Conditional Formatting with icon sets makes trends pop instantly.", "TEXTJOIN can merge cells with delimiters while skipping blanks.", "XLOOKUP replaces VLOOKUP/HLOOKUP with more power and cleaner syntax.", "FILTER + UNIQUE combo builds dynamic lists without helper columns.", ]

EXCEL_FUNCTIONS = [ ("XLOOKUP", "=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])"), ("FILTER", "=FILTER(array, include, [if_empty])"), ("UNIQUE", "=UNIQUE(array, [by_col], [exactly_once])"), ("TEXTSPLIT", "=TEXTSPLIT(text, col_delimiter, [row_delimiter])"), ("LET", "=LET(name1, value1, calculation)"), ("LAMBDA", "=LAMBDA(parameters, calculation)"), ("SUMIFS", "=SUMIFS(sum_range, criteria_range1, criteria1, [criteria_range2], [criteria2], ...)"), ("INDEX/MATCH", "=INDEX(return_range, MATCH(lookup_value, lookup_range, 0))"), ("IFERROR", "=IFERROR(value, value_if_error)"), ("SEQUENCE", "=SEQUENCE(rows, [columns], [start], [step])"), ]

POWERBI_TIPS = [ "Model star schemas when possible; avoid many-to-many unless needed.", "Hide technical columns from report view to reduce clutter.", "Use role-playing dates (Date table) with dedicated relationships.", "Keep visuals minimal; emphasize one insight per visual.", "Prefer measures over calculated columns when aggregating dynamic logic.", "Leverage field parameters to let users switch measures/dimensions.", "Optimize with aggregations or incremental refresh for large data.", "Use Performance Analyzer to spot slow visuals.", ]

DAX_SNIPPETS = [ ("Total Revenue", "Total Revenue = SUM(FactSales[Revenue])"), ("YoY Revenue", "YoY Revenue = CALCULATE([Total Revenue], DATEADD('Date'[Date], -1, YEAR))"), ("Running Total", "Running Total = CALCULATE([Total Revenue], FILTER(ALL('Date'), 'Date'[Date] <= MAX('Date'[Date])))"), ("Top N Customers", "Top Customers = TOPN(5, VALUES(Customers[Name]), [Total Revenue], DESC)"), ("Conversion Rate", "Conversion Rate = DIVIDE([Leads Won], [Leads Total])"), ]

POWER_QUERY_STEPS = [ "Source → Choose files/folders/databases.", "Promote Headers → Use first row as headers.", "Change Types → Ensure correct data types for each column.", "Split Column → By delimiter or number of characters.", "Merge Queries → Join datasets (Left/Right/Inner/Full).", "Append Queries → Stack tables vertically.", "Group By → Aggregate like sum/count/avg.", "Pivot/Unpivot → Reshape columns and rows.", "Fill Down/Up → Handle missing values.", "Remove Errors → Clean inconsistent rows.", ]

SHORTCUTS = [
    (
        "Excel",
        [
            ("Ctrl + Arrow", "Jump to data edges"),
            ("Ctrl + Shift + L", "Toggle filters"),
            ("Alt + =", "AutoSum"),
            ("Ctrl + 1", "Format Cells"),
            ("Ctrl + Shift + %", "Percent format"),
            ("Ctrl + '", "Copy value from cell above"),
            ("Ctrl + Enter", "Fill selected range with entry"),
        ],
    ),
    (
        "Power BI Desktop",
        [
            ("Ctrl + Shift + S", "Save As"),
            ("Ctrl + Shift + C", "Copy visual formatting"),
            ("F11", "Full screen focus"),
            ("Alt + Shift + Arrow", "Move visual small nudge"),
            ("Ctrl + .", "Selection pane"),
        ],
    ),
]

PROJECT_IDEAS = [ ("Retail Sales Dashboard", "Sales by product, region, month with cohort analysis."), ("HR Attrition Insights", "Headcount trend, attrition risk scoring, hiring funnel."), ("Financial Statement Analyzer", "Vertical/horizontal analysis, KPI cards, DuPont."), ("Marketing Funnel", "Impressions→Clicks→Leads→Wins with conversion DAX."), ("Inventory Health", "Stock turns, slow-moving SKUs, reorder points."), ("Customer 360", "RFM scoring, CLV estimation, churn signals."), ]

RESOURCE_LINKS = [ ("Official Excel Blog", "https://techcommunity.microsoft.com/t5/excel-blog/bg-p/ExcelBlog"), ("Power BI Blog", "https://powerbi.microsoft.com/en-us/blog/"), ("DAX Guide", "https://dax.guide"), ("VertiPaq Analyzer", "https://sqlbi.com/tools/vertipaq-analyzer/"), ("Power Query M Reference", "https://learn.microsoft.com/powerquery-m/"), ("Altair Docs", "https://altair-viz.github.io/"), ]

---------------------------------------------

Quiz Bank (Excel + Power BI)

---------------------------------------------

@dataclass class MCQ: question: str options: list[str] correct: int explanation: str

QUIZ: list[MCQ] = [ MCQ( "Which function replaces VLOOKUP and HLOOKUP with more flexibility?", ["MATCH", "XLOOKUP", "INDEX", "FILTER"], 1, "XLOOKUP handles vertical/horizontal lookups with simpler syntax and defaults.", ), MCQ( "In Power BI, which storage mode loads summarized values for performance?", ["DirectQuery", "Import", "Dual", "Aggregations"], 3, "Aggregations tables can answer at a summary level, improving performance.", ), MCQ( "Which DAX function safely handles division by zero?", ["DIVIDE", "SAFE_DIV", "COALESCE", "IFERROR"], 0, "DIVIDE(value, divisor, alternateResult) avoids errors when divisor is zero.", ), MCQ( "Power Query step to combine rows from two tables vertically is:", ["Merge Queries", "Append Queries", "Group By", "Expand"], 1, "Append stacks tables; Merge joins columns.", ), MCQ( "Excel shortcut to create a table from a range is:", ["Ctrl+Shift+T", "Ctrl+T", "Alt+T", "Ctrl+Shift+L"], 1, "Ctrl+T converts the selection to an Excel Table.", ), MCQ( "In a star schema, central table typically contains:", ["Dimension attributes", "Measures only", "Facts/transactions", "Only keys"], 2, "Fact table stores measures and keys to dimensions.", ), MCQ( "Which Excel function returns unique values from a range?", ["UNIQUE", "DISTINCT", "VALUES", "REMOVE.DUPES"], 0, "UNIQUE spills a distinct list from the source array.", ), MCQ( "Which Power BI feature lets users switch among measures in a visual?", ["Bookmarks", "Field parameters", "Themes", "Sync slicers"], 1, "Field parameters dynamically swap fields/measures in visuals.", ), MCQ( "Which DAX function shifts dates by periods?", ["DATEADD", "DATESYTD", "SAMEPERIODLASTYEAR", "PARALLELPERIOD"], 0, "DATEADD('Date'[Date], -1, YEAR) is classic for YoY.", ), MCQ( "Power Query operation to transform columns into rows is:", ["Pivot", "Unpivot", "Transpose", "Split"], 1, "Unpivot takes columns and turns them into attribute-value rows.", ), ]

---------------------------------------------

Reusable UI blocks

---------------------------------------------

def card(title: str, body: str | None = None, footer: str | None = None): with st.container(border=False): st.markdown(f"<div class='card'><h4>{title}</h4>", unsafe_allow_html=True) if body: st.markdown(body, unsafe_allow_html=True) if footer: st.markdown(f"<div class='divider'></div><div class='rownote'>{footer}</div>", unsafe_allow_html=True) st.markdown("</div>", unsafe_allow_html=True)

def vsp(px: int = 10): st.markdown(f"<div style='height:{px}px'></div>", unsafe_allow_html=True)

---------------------------------------------

Tabs

---------------------------------------------

TABS = st.tabs([ "Home", "Excel Basics", "Excel Functions", "Power Query", "Power BI Basics", "DAX Lab", "Charts Gallery", "Datasets", "Mini Projects", "Quiz", "Shortcuts", "Cheat Sheets", ])

---------------------------------------------

HOME TAB

---------------------------------------------

with TABS[0]: col1, col2 = st.columns([0.6, 0.4]) with col1: card( "Welcome", body=textwrap.dedent( f""" <p>Namaste, <b>{st.session_state.username}</b>! This colorful one-page learning hub brings together Excel and Power BI essentials: from basics to DAX, Power Query, visual best practices, interactive quizzes, and mini projects. Use the tabs above to explore.</p>

<ul>
                <li>🎨 Change the accent theme from the dropdown above.</li>
                <li>🧪 Try the DAX Lab - we mirror logic using pandas/Altair.</li>
                <li>🧠 Take the quiz - score ≥ 8/10 to unlock a certificate.</li>
                <li>⬇️ Download cheat sheets generated on the fly.</li>
            </ul>
            """
        ),
        footer="Built with Streamlit • No external APIs • Optimized for learning speed",
    )
    vsp(6)
    card(
        "Learning Roadmap (Quick)",
        body="""
        <ol>
            <li>Excel Fundamentals → Tables, Formatting, Lookups</li>
            <li>Excel Functions → Dynamic arrays, XLOOKUP, SUMIFS</li>
            <li>Power Query → Clean/shape data</li>
            <li>Power BI → Model, Relationships, Visual best practices</li>
            <li>DAX → Measures, Time Intelligence</li>
            <li>Projects → Build 2-3 end-to-end dashboards</li>
        </ol>
        """,
    )
with col2:
    card(
        "Practice Dataset Preview",
        body=sales_df.head().to_html(index=False),
        footer="Use the Datasets tab to download CSVs.",
    )
    vsp(6)
    st.markdown("### Quick KPI (Demo)")
    mcol1, mcol2, mcol3 = st.columns(3)
    with mcol1:
        card("Total Revenue", f"<h2>₹ {sales_df['Revenue'].sum():,}</h2>")
    with mcol2:
        card("Avg Price", f"<h2>₹ {int(sales_df['Price'].mean())}</h2>")
    with mcol3:
        card("People", f"<h2>{sales_df['Person'].nunique()}</h2>")

---------------------------------------------

EXCEL BASICS TAB

---------------------------------------------

with TABS[1]: st.markdown("### Excel Basics - Tables, Formatting, Lookups") c1, c2 = st.columns([0.6, 0.4]) with c1: card("Top Tips", "<ul>" + "".join([f"<li>{t}</li>" for t in EXCEL_TIPS]) + "</ul>") vsp(4) card( "Tables & Filtering Demo", body="Use the filter controls to slice the table.") # Interactive filter demo colf1, colf2, colf3 = st.columns(3) with colf1: m = st.selectbox("Month", ["(All)"] + months) with colf2: r = st.selectbox("Region", ["(All)"] + regions) with colf3: p = st.selectbox("Person", ["(All)"] + sorted(people)) df = sales_df.copy() if m != "(All)": df = df[df["Month"] == m] if r != "(All)": df = df[df["Region"] == r] if p != "(All)": df = df[df["Person"] == p] st.dataframe(df, use_container_width=True, height=320) with c2: card("Common Functions", "<ul>" + "".join([f"<li><b>{n}</b>: {f}</li>" for n, f in EXCEL_FUNCTIONS]) + "</ul>") vsp(4) # Simple Altair chart as Excel chart analog st.markdown("#### Monthly Revenue Trend (Demo Chart)") rev = sales_df.groupby("Month", as_index=False)["Revenue"].sum() # Preserve month order rev["Month"] = pd.Categorical(rev["Month"], categories=months, ordered=True) rev = rev.sort_values("Month") ch = alt.Chart(rev).mark_line(point=True).encode(x="Month", y="Revenue") st.altair_chart(ch, use_container_width=True)

---------------------------------------------

EXCEL FUNCTIONS TAB

---------------------------------------------

with TABS[2]: st.markdown("### Excel Functions - Hands-on Lab") left, right = st.columns([0.55, 0.45]) with left: card( "Lookup Playground (INDEX/MATCH style)", body="Use the selector to lookup a person's revenue in a chosen month.") target_month = st.selectbox("Select Month", months, index=0) target_person 